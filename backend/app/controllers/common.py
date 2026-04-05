from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.dependencies import get_current_user
from app.services import notification_service
from app.services.auth_service import hash_password, verify_password
from app.database import users_collection, notifications_collection
from bson import ObjectId
from datetime import datetime
import os, aiofiles
from app.config import settings

router = APIRouter()

def serialize_user(u):
    u["id"] = str(u["_id"]); del u["_id"]
    u.pop("password", None)
    return u

# ─── PROFILE ───
@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    u = await users_collection.find_one({"_id": ObjectId(user["id"])})
    return serialize_user(u)

@router.put("/profile")
async def update_profile(data: dict, user=Depends(get_current_user)):
    allowed = {k: v for k, v in data.items() if k in ["name", "phone"]}
    await users_collection.update_one({"_id": ObjectId(user["id"])}, {"$set": allowed})
    u = await users_collection.find_one({"_id": ObjectId(user["id"])})
    return serialize_user(u)

@router.put("/profile/password")
async def change_password(data: dict, user=Depends(get_current_user)):
    u = await users_collection.find_one({"_id": ObjectId(user["id"])})
    if not verify_password(data.get("current_password", ""), u["password"]):
        raise HTTPException(400, "Current password is incorrect")
    new_pass = data.get("new_password", "")
    confirm = data.get("confirm_password", "")
    if new_pass != confirm:
        raise HTTPException(400, "New passwords do not match")
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"password": hash_password(new_pass)}}
    )
    return {"message": "Password changed successfully"}

@router.post("/profile/picture")
async def upload_profile_pic(file: UploadFile = File(...), user=Depends(get_current_user)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filename = f"profile_{user['id']}_{int(datetime.utcnow().timestamp())}{os.path.splitext(file.filename)[1]}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    async with aiofiles.open(filepath, "wb") as f:
        content = await file.read()
        await f.write(content)
    image_url = f"/uploads/{filename}"
    await users_collection.update_one({"_id": ObjectId(user["id"])}, {"$set": {"profile_pic": image_url}})
    return {"profile_pic": image_url}

# ─── NOTIFICATIONS ───
@router.get("/notifications")
async def get_notifications(user=Depends(get_current_user)):
    return await notification_service.get_notifications(user["id"])

@router.put("/notifications/read")
async def mark_all_read(user=Depends(get_current_user)):
    await notification_service.mark_all_read(user["id"])
    return {"message": "All notifications marked as read"}

@router.put("/notifications/{notif_id}/read")
async def mark_one_read(notif_id: str, user=Depends(get_current_user)):
    await notification_service.mark_one_read(notif_id)
    return {"message": "Notification marked as read"}

@router.delete("/notifications/{notif_id}")
async def delete_notification(notif_id: str, user=Depends(get_current_user)):
    await notification_service.delete_notification(notif_id)
    return {"message": "Notification deleted"}

# ─── SETTINGS ───
@router.get("/settings")
async def get_settings(user=Depends(get_current_user)):
    u = await users_collection.find_one({"_id": ObjectId(user["id"])})
    return u.get("settings", {})

@router.put("/settings")
async def update_settings(data: dict, user=Depends(get_current_user)):
    await users_collection.update_one({"_id": ObjectId(user["id"])}, {"$set": {"settings": data}})
    return {"message": "Settings updated", "settings": data}
