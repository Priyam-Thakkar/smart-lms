from app.database import hubs_collection
from datetime import datetime
from bson import ObjectId

def serialize_hub(h: dict) -> dict:
    h["id"] = str(h["_id"])
    del h["_id"]
    return h

async def create_hub(data: dict) -> dict:
    data["created_at"] = datetime.utcnow()
    result = await hubs_collection.insert_one(data)
    hub = await hubs_collection.find_one({"_id": result.inserted_id})
    return serialize_hub(hub)

async def get_all_hubs() -> list:
    hubs = []
    async for h in hubs_collection.find():
        hubs.append(serialize_hub(h))
    return hubs

async def get_hub_by_id(hub_id: str) -> dict:
    h = await hubs_collection.find_one({"_id": ObjectId(hub_id)})
    if h:
        return serialize_hub(h)
    return None

async def update_hub(hub_id: str, data: dict) -> dict:
    await hubs_collection.update_one({"_id": ObjectId(hub_id)}, {"$set": data})
    return await get_hub_by_id(hub_id)

async def delete_hub(hub_id: str) -> bool:
    result = await hubs_collection.delete_one({"_id": ObjectId(hub_id)})
    return result.deleted_count > 0
