from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Existing models (keep your current TextRequest and PredictionResponse)
class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: Dict[str, float]

# User Authentication Models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "password": "securepassword123"
            }
        }

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    created_at: datetime
    is_active: bool = True

class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str
    created_at: datetime
    is_active: bool
    total_analyses: int = 0

# News Analysis Models
class NewsAnalysis(BaseModel):
    id: Optional[str] = None
    text: str
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    analyzed_at: datetime
    user_id: Optional[str] = None

class NewsAnalysisCreate(BaseModel):
    text: str

class NewsAnalysisResponse(BaseModel):
    id: str
    text: str
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    analyzed_at: datetime

# Authentication Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Response Models
class MessageResponse(BaseModel):
    message: str
    
class HistoryResponse(BaseModel):
    history: List[NewsAnalysisResponse]
    total_count: int
    
class StatsResponse(BaseModel):
    total_analyses: int
    fake_count: int
    real_count: int
    average_confidence: float
