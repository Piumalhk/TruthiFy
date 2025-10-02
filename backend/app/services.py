from datetime import datetime, timedelta
from .auth import get_password_hash, verify_password, create_access_token
from app.database import get_database
from typing import List, Tuple
from bson import ObjectId
from fastapi import HTTPException

class UserService:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user_data):
        """Create a new user"""
        # Check if username already exists
        existing_user = await self.db.users.find_one({"username": user_data.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Check if email already exists
        existing_email = await self.db.users.find_one({"email": user_data.email})
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        # Create user document
        user_doc = {
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "password": get_password_hash(user_data.password),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        result = await self.db.users.insert_one(user_doc)
        return str(result.inserted_id)

    async def authenticate_user(self, username: str, password: str):
        """Authenticate user with username and password"""
        user = await self.db.users.find_one({"username": username})
        if not user:
            return False
        
        if not verify_password(password, user["password"]):
            return False
        
        return user

    async def create_access_token_for_user(self, username: str):
        """Create access token for user"""
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return access_token

    async def get_user_stats(self, user_id: str):
        # Count total analyses
        total_analyses = await self.db.history.count_documents({"user_id": user_id})
        
        # Count fake and real predictions
        fake_count = await self.db.history.count_documents({
            "user_id": user_id, 
            "prediction": "FAKE"
        })
        real_count = await self.db.history.count_documents({
            "user_id": user_id, 
            "prediction": "REAL"
        })
        
        # Calculate average confidence
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": None, "avg_confidence": {"$avg": "$confidence"}}}
        ]
        
        result = await self.db.history.aggregate(pipeline).to_list(1)
        avg_confidence = result[0]["avg_confidence"] if result else 0.0

        return {
            "total_analyses": total_analyses,
            "fake_count": fake_count,
            "real_count": real_count,
            "average_confidence": round(avg_confidence, 4)
        }


# ✅ Add this new service for saving analyses

class AnalysisService:
    def __init__(self, db):
        self.db = db

    async def save_analysis(self, text: str, prediction: str, confidence: float, probabilities: dict, user_id: str) -> str:
        """Save news analysis to database"""
        analysis_doc = {
            "text": text,
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": probabilities,
            "user_id": user_id,
            "analyzed_at": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        
        result = await self.db.history.insert_one(analysis_doc)
        return str(result.inserted_id)

    async def get_user_history(self, user_id: str, limit: int, skip: int) -> Tuple[List[dict], int]:
        # Query MongoDB for history belonging to this user
        cursor = self.db.history.find({"user_id": user_id}).sort("analyzed_at", -1).skip(skip).limit(limit)
        history = await cursor.to_list(length=limit)

        # Convert ObjectId to string and format for response
        formatted_history = []
        for item in history:
            formatted_item = {
                "id": str(item["_id"]),
                "user_id": str(item["user_id"]),
                "text": item["text"],
                "prediction": item["prediction"],
                "confidence": item["confidence"],
                "probabilities": item["probabilities"],
                "analyzed_at": item["analyzed_at"],
                "created_at": item.get("created_at", item["analyzed_at"])
            }
            formatted_history.append(formatted_item)

        total_count = await self.db.history.count_documents({"user_id": user_id})
        return formatted_history, total_count

    async def get_analysis_by_id(self, analysis_id: str, user_id: str):
        analysis = await self.db.history.find_one({"_id": ObjectId(analysis_id), "user_id": user_id})
        if analysis:
            return {
                "id": str(analysis["_id"]),
                "user_id": str(analysis["user_id"]),
                "text": analysis["text"],
                "prediction": analysis["prediction"],
                "confidence": analysis["confidence"],
                "probabilities": analysis["probabilities"],
                "analyzed_at": analysis["analyzed_at"],
                "created_at": analysis.get("created_at", analysis["analyzed_at"])
            }
        return None

    async def delete_analysis(self, analysis_id: str, user_id: str) -> bool:
        result = await self.db.history.delete_one({"_id": ObjectId(analysis_id), "user_id": user_id})
        return result.deleted_count > 0

    async def clear_user_history(self, user_id: str) -> int:
        result = await self.db.history.delete_many({"user_id": user_id})
        return result.deleted_count
