"""
Seed Data Script for Smart LMS
Run this ONCE to create demo users in MongoDB.
Usage: python seed_data.py
"""
import asyncio
import bcrypt
import motor.motor_asyncio
from datetime import datetime

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "lms_db"


def hash_pw(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


async def seed():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    users_col = db["users"]

    # Test connection
    try:
        await client.admin.command("ping")
        print("MongoDB connected OK\n")
    except Exception as e:
        print(f"ERROR: Cannot connect to MongoDB: {e}")
        return

    demo_users = [
        ("Admin User",    "admin@lms.com",    "admin123",    "admin"),
        ("Agent User",    "agent@lms.com",    "agent123",    "agent"),
        ("Customer User", "customer@lms.com", "customer123", "customer"),
    ]

    for name, email, password, role in demo_users:
        hashed = hash_pw(password)
        existing = await users_col.find_one({"email": email})
        if existing:
            # Update password hash in case it was created with passlib
            await users_col.update_one({"email": email}, {"$set": {"password": hashed}})
            print(f"Updated: {email} ({role})")
        else:
            await users_col.insert_one({
                "name": name,
                "email": email,
                "password": hashed,
                "role": role,
                "phone": None,
                "profile_pic": None,
                "created_at": datetime.utcnow(),
                "settings": {
                    "notifications_enabled": True,
                    "email_alerts": True,
                    "language": "en"
                }
            })
            print(f"Created: {email} / {password} ({role})")

    print("\nSeed complete!")
    print("Credentials:")
    print("  Admin    : admin@lms.com    / admin123")
    print("  Agent    : agent@lms.com    / agent123")
    print("  Customer : customer@lms.com / customer123")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
