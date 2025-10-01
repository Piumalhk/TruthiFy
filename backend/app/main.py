from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import connect_to_mongo, close_mongo_connection
from .models import (
    TextRequest, PredictionResponse, UserCreate, UserLogin, 
    Token, NewsAnalysisCreate, MessageResponse, HistoryResponse, StatsResponse
)
from .services import UserService, AnalysisService
from .auth import get_current_active_user
from .model import FakeNewsModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="TruthiFy API", 
    description="Fake News Detection API with User Management", 
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
user_service = UserService()
analysis_service = AnalysisService()

# Initialize model (this might take a while on first run)
try:
    model = FakeNewsModel()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

@app.get("/")
async def root():
    return {"message": "TruthiFy API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "database": "connected"
    }

# Authentication Endpoints
@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        user_id = await user_service.create_user(user_data)
        return MessageResponse(message=f"User {user_data.username} created successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/login", response_model=Token)
async def login_user(user_data: UserLogin):
    """Login user and return access token"""
    user = await user_service.authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await user_service.create_access_token_for_user(user["username"])
    return Token(access_token=access_token, token_type="bearer")

# News Analysis Endpoints
@app.post("/predict", response_model=PredictionResponse)
async def predict_fake_news(
    request: TextRequest, 
    current_user: dict = Depends(get_current_active_user)
):
    """Analyze news text and save to user history"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        result = model.predict(request.text)
        
        if result.get("prediction") == "ERROR":
            raise HTTPException(status_code=500, detail=f"Prediction error: {result.get('error')}")
        
        # Save analysis to database
        await analysis_service.save_analysis(
            text=request.text,
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            user_id=str(current_user["_id"])
        )
        
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

# User Profile and History Endpoints
@app.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_active_user)):
    """Get current user profile with statistics"""
    user_stats = await user_service.get_user_stats(str(current_user["_id"]))
    
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "created_at": current_user["created_at"],
        "is_active": current_user["is_active"],
        "stats": user_stats
    }

@app.get("/history", response_model=HistoryResponse)
async def get_analysis_history(
    limit: int = 20,
    skip: int = 0,
    current_user: dict = Depends(get_current_active_user)
):
    """Get user's analysis history"""
    try:
        history, total_count = await analysis_service.get_user_history(
            str(current_user["_id"]), limit=limit, skip=skip
        )
        return HistoryResponse(history=history, total_count=total_count)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analysis history")

@app.delete("/history/{analysis_id}", response_model=MessageResponse)
async def delete_analysis(
    analysis_id: str, 
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a specific analysis from user's history"""
    try:
        deleted = await analysis_service.delete_analysis(analysis_id, str(current_user["_id"]))
        if not deleted:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return MessageResponse(message="Analysis deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete analysis")

@app.get("/stats", response_model=StatsResponse)
async def get_user_stats(current_user: dict = Depends(get_current_active_user)):
    """Get user's analysis statistics"""
    try:
        stats = await user_service.get_user_stats(str(current_user["_id"]))
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Failed to fetch stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")

# Model Information Endpoint
@app.get("/models/info")
async def model_info():
    """Get information about the loaded model"""
    if model is None:
        return {"error": "Model not loaded"}
    
    return {
        "model_name": "hamzab/roberta-fake-news-classification",
        "device": str(model.device),
        "status": "loaded"
    }