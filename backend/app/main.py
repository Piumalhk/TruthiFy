from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .model import FakeNewsModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TruthiFy API", description="Fake News Detection API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model (this might take a while on first run)
try:
    model = FakeNewsModel()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict

@app.get("/")
async def root():
    return {"message": "TruthiFy API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_fake_news(request: TextRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
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
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

@app.get("/models/info")
async def model_info():
    if model is None:
        return {"error": "Model not loaded"}
    
    return {
        "model_name": "hamzab/roberta-fake-news-classification",
        "device": str(model.device),
        "status": "loaded"
    }