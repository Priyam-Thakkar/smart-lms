import motor.motor_asyncio
from app.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DB_NAME]

# Collections
users_collection = db["users"]
parcels_collection = db["parcels"]
hubs_collection = db["hubs"]
routes_collection = db["routes"]
dispatches_collection = db["dispatches"]
billing_collection = db["billing"]
tickets_collection = db["tickets"]
notifications_collection = db["notifications"]

async def create_indexes():
    """Create MongoDB indexes for performance"""
    # Users
    await users_collection.create_index("email", unique=True)
    await users_collection.create_index("role")
    # Parcels
    await parcels_collection.create_index("tracking_id")
    await parcels_collection.create_index("assigned_agent_id")
    await parcels_collection.create_index("status")
    # Tickets
    await tickets_collection.create_index("customer_id")
    await tickets_collection.create_index("parcel_id")
    # Billing
    await billing_collection.create_index("parcel_id")
    await billing_collection.create_index("payment_status")
    # Dispatches
    await dispatches_collection.create_index("parcel_id")
    await dispatches_collection.create_index("agent_id")
    # Notifications
    await notifications_collection.create_index("user_id")
    await notifications_collection.create_index("is_read")
