from app.database import billing_collection
from datetime import datetime
from bson import ObjectId
import random
import string

def generate_invoice_number() -> str:
    year = datetime.now().year
    number = ''.join(random.choices(string.digits, k=5))
    return f"INV-{year}-{number}"

def serialize_billing(b: dict) -> dict:
    b["id"] = str(b["_id"])
    del b["_id"]
    return b

async def create_billing(parcel_id: str, customer_name: str, customer_email: str, amount: float) -> dict:
    invoice_number = generate_invoice_number()
    doc = {
        "invoice_number": invoice_number,
        "parcel_id": parcel_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "amount": amount,
        "payment_status": "Unpaid",
        "generated_at": datetime.utcnow(),
        "paid_at": None,
        "pdf_path": None
    }
    result = await billing_collection.insert_one(doc)
    billing = await billing_collection.find_one({"_id": result.inserted_id})
    return serialize_billing(billing)

async def get_all_billing() -> list:
    billings = []
    async for b in billing_collection.find().sort("generated_at", -1):
        billings.append(serialize_billing(b))
    return billings

async def get_billing_by_id(billing_id: str) -> dict:
    b = await billing_collection.find_one({"_id": ObjectId(billing_id)})
    if b:
        return serialize_billing(b)
    return None

async def get_billing_by_parcel_id(parcel_id: str) -> dict:
    b = await billing_collection.find_one({"parcel_id": parcel_id})
    if b:
        return serialize_billing(b)
    return None

async def mark_paid(billing_id: str) -> dict:
    await billing_collection.update_one(
        {"_id": ObjectId(billing_id)},
        {"$set": {"payment_status": "Paid", "paid_at": datetime.utcnow()}}
    )
    return await get_billing_by_id(billing_id)
