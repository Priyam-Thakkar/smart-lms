from app.database import notifications_collection
from datetime import datetime
from bson import ObjectId

async def create_notification(user_id: str, message: str, notif_type: str = "system"):
    doc = {
        "user_id": user_id,
        "message": message,
        "type": notif_type,
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    await notifications_collection.insert_one(doc)

async def get_notifications(user_id: str) -> list:
    notifs = []
    async for n in notifications_collection.find({"user_id": user_id}).sort("created_at", -1):
        n["id"] = str(n["_id"])
        del n["_id"]
        notifs.append(n)
    return notifs

async def mark_all_read(user_id: str):
    await notifications_collection.update_many(
        {"user_id": user_id, "is_read": False},
        {"$set": {"is_read": True}}
    )

async def mark_one_read(notif_id: str):
    await notifications_collection.update_one(
        {"_id": ObjectId(notif_id)},
        {"$set": {"is_read": True}}
    )

async def delete_notification(notif_id: str):
    await notifications_collection.delete_one({"_id": ObjectId(notif_id)})
