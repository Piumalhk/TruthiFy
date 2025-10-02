# app/database.py

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://User:2310d3Xc7SdVkKc1@cluster0.zhboudq.mongodb.net/Truthify?retryWrites=true&w=majority&ssl=true&tlsAllowInvalidCertificates=true")


_db = None  # Global database reference

async def connect_to_mongo():
    """Connect to MongoDB and store the database instance in _db"""
    global _db
    try:
        client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Ping the server to verify connection
        await client.admin.command("ping")
        _db = client.get_default_database()
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close MongoDB connection"""
    global _db
    if _db is not None:
        _db.client.close()
        _db = None
        print("✅ MongoDB connection closed")

def get_database():
    """Return the connected MongoDB database"""
    if _db is None:  # ✅ explicit check
        raise Exception("Database not connected. Call connect_to_mongo() first.")
    return _db
