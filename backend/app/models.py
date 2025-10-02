from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
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

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if len(v) > 72:
            raise ValueError('Password cannot be longer than 72 characters')
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (exceeds 72 bytes when encoded)')
        return v

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username cannot be longer than 50 characters')
        return v

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
    
class HistoryItem(BaseModel):
    id: str
    user_id: str
    text: str
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    analyzed_at: datetime
    created_at: Optional[datetime] = None

class HistoryResponse(BaseModel):
    history: List[HistoryItem]
    total_count: int

class StatsResponse(BaseModel):
    total_analyses: int
    fake_count: int
    real_count: int
    average_confidence: float
    average_confidence: float
