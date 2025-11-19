# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class HistoryItem(BaseModel):
    text: str
    prediction: str
    confidence: float
    timestamp: datetime

class AnalyzeRequest(BaseModel):
    text: str
