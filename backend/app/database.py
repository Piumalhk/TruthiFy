from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Truthify")

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(MONGODB_URL)
        db.database = db.client[DATABASE_NAME]
        
        # Test the connection
        await db.client.admin.command('ping')
        print(f"✅ Connected to MongoDB database: {DATABASE_NAME}")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("🔌 Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return db.database

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Create indexes for users collection
        await db.database.users.create_index("username", unique=True)
        await db.database.users.create_index("email", unique=True)
        
        # Create indexes for analyses collection
        await db.database.analyses.create_index([("user_id", 1), ("analyzed_at", -1)])
        await db.database.analyses.create_index("analyzed_at")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not create indexes: {e}")
