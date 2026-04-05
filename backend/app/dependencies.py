from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import decode_access_token
from app.database import users_collection
from bson import ObjectId

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user["id"] = str(user["_id"])
    return user

async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

async def require_agent(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "agent":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Agent access required")
    return current_user

async def require_customer(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer access required")
    return current_user
