from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.models.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.database import users_collection
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.config import settings
from datetime import datetime

router = APIRouter()

def serialize_user(u: dict) -> dict:
    u["id"] = str(u["_id"])
    del u["_id"]
    return u

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    token = create_access_token(
        {"sub": str(user["_id"]), "role": user["role"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    user_data = serialize_user(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(**user_data)
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate):
    existing = await users_collection.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": data.role,
        "phone": data.phone,
        "profile_pic": None,
        "created_at": datetime.utcnow(),
        "settings": {
            "theme": "blue-white",
            "notifications_enabled": True,
            "email_alerts": True,
            "language": "en"
        }
    }
    result = await users_collection.insert_one(user_doc)
    return {"message": "User registered successfully", "id": str(result.inserted_id)}
