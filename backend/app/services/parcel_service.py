from app.database import parcels_collection
from datetime import datetime
from bson import ObjectId
import random
import string

def generate_tracking_id() -> str:
    year = datetime.now().year
    number = ''.join(random.choices(string.digits, k=5))
    return f"LMS-{year}-{number}"

def serialize_parcel(parcel: dict) -> dict:
    parcel["id"] = str(parcel["_id"])
    del parcel["_id"]
    if "assigned_agent_id" in parcel and parcel["assigned_agent_id"]:
        parcel["assigned_agent_id"] = str(parcel["assigned_agent_id"])
    return parcel

async def create_parcel(data: dict, created_by: str) -> dict:
    data["tracking_id"] = generate_tracking_id()
    data["status"] = "Created"
    data["status_history"] = [{"status": "Created", "timestamp": datetime.utcnow(), "updated_by": created_by}]
    data["proof_of_delivery"] = None
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    result = await parcels_collection.insert_one(data)
    parcel = await parcels_collection.find_one({"_id": result.inserted_id})
    return serialize_parcel(parcel)

async def get_all_parcels(filters: dict = {}) -> list:
    parcels = []
    async for parcel in parcels_collection.find(filters):
        parcels.append(serialize_parcel(parcel))
    return parcels

async def get_parcel_by_id(parcel_id: str) -> dict:
    parcel = await parcels_collection.find_one({"_id": ObjectId(parcel_id)})
    if parcel:
        return serialize_parcel(parcel)
    return None

async def get_parcel_by_tracking_id(tracking_id: str) -> dict:
    parcel = await parcels_collection.find_one({"tracking_id": tracking_id})
    if parcel:
        return serialize_parcel(parcel)
    return None

async def update_parcel(parcel_id: str, data: dict) -> dict:
    data["updated_at"] = datetime.utcnow()
    await parcels_collection.update_one({"_id": ObjectId(parcel_id)}, {"$set": data})
    return await get_parcel_by_id(parcel_id)

async def update_parcel_status(parcel_id: str, status: str, updated_by: str) -> dict:
    status_entry = {"status": status, "timestamp": datetime.utcnow(), "updated_by": updated_by}
    await parcels_collection.update_one(
        {"_id": ObjectId(parcel_id)},
        {
            "$set": {"status": status, "updated_at": datetime.utcnow()},
            "$push": {"status_history": status_entry}
        }
    )
    return await get_parcel_by_id(parcel_id)

async def assign_agent(parcel_id: str, agent_id: str) -> dict:
    await parcels_collection.update_one(
        {"_id": ObjectId(parcel_id)},
        {"$set": {"assigned_agent_id": agent_id, "updated_at": datetime.utcnow()}}
    )
    return await get_parcel_by_id(parcel_id)

async def save_proof_of_delivery(parcel_id: str, image_url: str) -> dict:
    proof = {"image_url": image_url, "uploaded_at": datetime.utcnow()}
    await parcels_collection.update_one(
        {"_id": ObjectId(parcel_id)},
        {"$set": {"proof_of_delivery": proof, "updated_at": datetime.utcnow()}}
    )
    return await get_parcel_by_id(parcel_id)

async def delete_parcel(parcel_id: str) -> bool:
    result = await parcels_collection.delete_one({"_id": ObjectId(parcel_id)})
    return result.deleted_count > 0
