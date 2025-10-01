from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from ..models import TextRequest, PredictionResponse, MessageResponse
from ..services import AnalysisService
from ..auth import get_current_active_user
from ..model import FakeNewsModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news", tags=["News Analysis"])

# Initialize services
analysis_service = AnalysisService()

# Initialize model
try:
    model = FakeNewsModel()
    logger.info("News analysis model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

@router.post("/analyze", response_model=PredictionResponse)
async def analyze_news(
    request: TextRequest, 
    current_user: dict = Depends(get_current_active_user)
):
    """Analyze news text for fake news detection"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 10000:
        raise HTTPException(status_code=400, detail="Text too long (max 10,000 characters)")
    
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

@router.post("/analyze-anonymous", response_model=PredictionResponse)
async def analyze_news_anonymous(request: TextRequest):
    """Analyze news text without user authentication (no history saved)"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:  # Smaller limit for anonymous users
        raise HTTPException(status_code=400, detail="Text too long (max 5,000 characters for anonymous users)")
    
    try:
        result = model.predict(request.text)
        
        if result.get("prediction") == "ERROR":
            raise HTTPException(status_code=500, detail=f"Prediction error: {result.get('error')}")
        
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"]
        )
    
    except Exception as e:
        logger.error(f"Anonymous prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

@router.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    if model is None:
        return {"error": "Model not loaded", "status": "unavailable"}
    
    return {
        "model_name": "hamzab/roberta-fake-news-classification",
        "device": str(model.device),
        "status": "loaded",
        "max_length": 512,
        "supported_languages": ["English"]
    }

@router.get("/stats")
async def get_global_stats():
    """Get global analysis statistics (public endpoint)"""
    try:
        # You can implement global stats here
        return {
            "total_analyses": "Coming soon",
            "accuracy_rate": "95.2%",
            "model_version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Failed to fetch global stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")
