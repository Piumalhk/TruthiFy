from datetime import datetime
from .auth import get_password_hash, verify_password, create_access_token
from app.database import get_database


class UserService:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user_data):
        hashed_password = get_password_hash(user_data.password)
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "password": hashed_password,
            "full_name": user_data.full_name,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        result = await self.db.users.insert_one(user_dict)
        return str(result.inserted_id)

    async def authenticate_user(self, username: str, password: str):
        user = await self.db.users.find_one({"username": username})
        if user and verify_password(password, user["password"]):
            return user
        return None

    async def create_access_token_for_user(self, username: str):
        return create_access_token({"sub": username})

    async def get_user_stats(self, user_id: str):
        # Example placeholder
        return {"logins": 10, "actions": 25}


# ✅ Add this new service for saving analyses
class AnalysisService:
    def __init__(self, db):
        self.db = db
        self.collection = self.db.get_collection("analyses")

    async def save_analysis(self, text, prediction, confidence, probabilities, user_id):
        analysis_doc = {
            "text": text,
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": probabilities,
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }
        result = await self.collection.insert_one(analysis_doc)
        return str(result.inserted_id)

    async def get_user_history(self, user_id, limit=50, skip=0):
        """Get user's analysis history with pagination"""
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
        history = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            history.append(doc)
        
        total_count = await self.collection.count_documents({"user_id": user_id})
        return history, total_count

    async def get_analysis_by_id(self, analysis_id, user_id):
        """Get specific analysis by ID"""
        from bson import ObjectId
        try:
            doc = await self.collection.find_one({"_id": ObjectId(analysis_id), "user_id": user_id})
            if doc:
                doc["id"] = str(doc["_id"])
                del doc["_id"]
            return doc
        except:
            return None

    async def delete_analysis(self, analysis_id, user_id):
        """Delete specific analysis"""
        from bson import ObjectId
        try:
            result = await self.collection.delete_one({"_id": ObjectId(analysis_id), "user_id": user_id})
            return result.deleted_count > 0
        except:
            return False

    async def clear_user_history(self, user_id):
        """Clear all user's analysis history"""
        result = await self.collection.delete_many({"user_id": user_id})
        return result.deleted_count
