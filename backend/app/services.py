from datetime import datetime, timedelta
from typing import Optional, List
from .database import get_database
from .models import UserCreate, NewsAnalysis
from .auth import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.db = None
    
    async def get_db(self):
        if not self.db:
            self.db = get_database()
        return self.db

    async def create_user(self, user_data: UserCreate):
        """Create a new user"""
        db = await self.get_db()
        
        # Check if user already exists
        existing_user = await db.users.find_one({
            "$or": [
                {"username": user_data.username},
                {"email": user_data.email}
            ]
        })
        
        if existing_user:
            if existing_user["username"] == user_data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create new user
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": get_password_hash(user_data.password),
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        try:
            result = await db.users.insert_one(user_dict)
            logger.info(f"User created successfully: {user_data.username}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )

    async def authenticate_user(self, username: str, password: str):
        """Authenticate user with username and password"""
        db = await self.get_db()
        user = await db.users.find_one({"username": username})
        
        if not user or not verify_password(password, user["hashed_password"]):
            return False
        return user

    async def create_access_token_for_user(self, username: str):
        """Create access token for user"""
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return access_token

    async def get_user_by_username(self, username: str):
        """Get user by username"""
        db = await self.get_db()
        user = await db.users.find_one({"username": username})
        return user

    async def get_user_stats(self, user_id: str):
        """Get user statistics"""
        db = await self.get_db()
        
        # Count total analyses
        total_analyses = await db.analyses.count_documents({"user_id": user_id})
        
        # Count fake and real predictions
        fake_count = await db.analyses.count_documents({
            "user_id": user_id, 
            "prediction": "FAKE"
        })
        real_count = await db.analyses.count_documents({
            "user_id": user_id, 
            "prediction": "REAL"
        })
        
        # Calculate average confidence
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": None, "avg_confidence": {"$avg": "$confidence"}}}
        ]
        
        result = await db.analyses.aggregate(pipeline).to_list(1)
        avg_confidence = result[0]["avg_confidence"] if result else 0.0
        
        return {
            "total_analyses": total_analyses,
            "fake_count": fake_count,
            "real_count": real_count,
            "average_confidence": round(avg_confidence, 4)
        }

class AnalysisService:
    def __init__(self):
        self.db = None
    
    async def get_db(self):
        if not self.db:
            self.db = get_database()
        return self.db

    async def save_analysis(self, text: str, prediction: str, confidence: float, 
                          probabilities: dict, user_id: Optional[str] = None):
        """Save news analysis to database"""
        db = await self.get_db()
        
        analysis_dict = {
            "text": text,
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": probabilities,
            "analyzed_at": datetime.utcnow(),
            "user_id": user_id
        }
        
        try:
            result = await db.analyses.insert_one(analysis_dict)
            logger.info(f"Analysis saved for user: {user_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save analysis"
            )

    async def get_user_history(self, user_id: str, limit: int = 50, skip: int = 0):
        """Get user's analysis history"""
        db = await self.get_db()
        
        try:
            cursor = db.analyses.find({"user_id": user_id}).sort("analyzed_at", -1).skip(skip).limit(limit)
            analyses = []
            
            async for analysis in cursor:
                analysis["id"] = str(analysis["_id"])
                del analysis["_id"]
                analyses.append(analysis)
            
            # Get total count
            total_count = await db.analyses.count_documents({"user_id": user_id})
            
            return analyses, total_count
        except Exception as e:
            logger.error(f"Error fetching user history: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch analysis history"
            )

    async def delete_analysis(self, analysis_id: str, user_id: str):
        """Delete user's analysis"""
        db = await self.get_db()
        
        try:
            result = await db.analyses.delete_one({
                "_id": ObjectId(analysis_id),
                "user_id": user_id
            })
            
            if result.deleted_count > 0:
                logger.info(f"Analysis deleted: {analysis_id} for user: {user_id}")
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error deleting analysis: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete analysis"
            )

    async def get_analysis_by_id(self, analysis_id: str, user_id: str):
        """Get specific analysis by ID"""
        db = await self.get_db()
        
        try:
            analysis = await db.analyses.find_one({
                "_id": ObjectId(analysis_id),
                "user_id": user_id
            })
            
            if analysis:
                analysis["id"] = str(analysis["_id"])
                del analysis["_id"]
            
            return analysis
        except Exception as e:
            logger.error(f"Error fetching analysis: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch analysis"
            )

    async def clear_user_history(self, user_id: str):
        """Clear all analysis history for a user"""
        db = await self.get_db()
        
        try:
            result = await db.analyses.delete_many({"user_id": user_id})
            logger.info(f"Cleared {result.deleted_count} analyses for user: {user_id}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error clearing user history: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to clear user history"
            )
