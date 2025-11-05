# database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://User:imCQq6Uw4n3xkR9s@cluster0.zhboudq.mongodb.net/Truthify?retryWrites=true&w=majority")
client = AsyncIOMotorClient(MONGO_URI)
db = client.Truthify

users_collection = db.users
history_collection = db.history