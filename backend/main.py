# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model.fake_news_model import load_model
import json

# Initialize FastAPI
app = FastAPI(title="Fake News Detection API", version="2.0")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model once at startup
pipe = load_model()

# Pydantic models for request validation
class NewsAnalysisRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Fake News Detection API is running 🚀"}

@app.post("/predict")
async def predict(request: Request):
    try:
        # Try to get JSON data
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="Request body is empty")
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        
        text = data.get("text", "")

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text provided")

        result = pipe(text)[0]
        label = result["label"]
        score = round(result["score"], 3)

        return {
            "label": label,
            "confidence": score
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Add the API v1 endpoints that the frontend expects
@app.post("/api/v1/news/analyze")
async def analyze_news_authenticated(news_request: NewsAnalysisRequest):
    """Analyze news for authenticated users"""
    try:
        text = news_request.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        result = pipe(text)[0]
        label = result["label"]
        score = round(result["score"], 3)

        # Calculate probabilities for both REAL and FAKE
        if label == "FAKE":
            fake_prob = score
            real_prob = 1 - score
        else:
            real_prob = score
            fake_prob = 1 - score

        return {
            "prediction": label,
            "confidence": score,
            "probabilities": {
                "REAL": round(real_prob, 3),
                "FAKE": round(fake_prob, 3)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/v1/news/analyze-anonymous")
async def analyze_news_anonymous(news_request: NewsAnalysisRequest):
    """Analyze news for anonymous users"""
    try:
        text = news_request.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        result = pipe(text)[0]
        label = result["label"]
        score = round(result["score"], 3)

        # Calculate probabilities for both REAL and FAKE
        if label == "FAKE":
            fake_prob = score
            real_prob = 1 - score
        else:
            real_prob = score
            fake_prob = 1 - score

        return {
            "prediction": label,
            "confidence": score,
            "probabilities": {
                "REAL": round(real_prob, 3),
                "FAKE": round(fake_prob, 3)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Auth endpoints (stubs - will need proper implementation later)
@app.post("/api/v1/auth/register")
async def register():
    return {"message": "Registration endpoint - not implemented yet"}

@app.post("/api/v1/auth/login")
async def login():
    return {"message": "Login endpoint - not implemented yet"}

@app.get("/api/v1/auth/me")
async def get_current_user():
    return {"message": "Current user endpoint - not implemented yet"}

@app.get("/api/v1/auth/profile")
async def get_profile():
    return {"message": "Profile endpoint - not implemented yet"}

@app.post("/api/v1/auth/logout")
async def logout():
    return {"message": "Logout endpoint - not implemented yet"}

# History endpoints (stubs)
@app.get("/api/v1/history")
async def get_history():
    return {"history": [], "message": "History endpoint - not implemented yet"}

@app.get("/api/v1/history/stats")
async def get_stats():
    return {"total_analyses": 0, "fake_count": 0, "real_count": 0, "message": "Stats endpoint - not implemented yet"}

@app.delete("/api/v1/history/{analysis_id}")
async def delete_analysis(analysis_id: str):
    return {"message": f"Delete analysis {analysis_id} - not implemented yet"}

@app.delete("/api/v1/history")
async def clear_history():
    return {"message": "Clear history endpoint - not implemented yet"}

# System health endpoints
@app.get("/api/v1/system/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/v1/system/info")
async def system_info():
    return {"version": "2.0", "model": "ghanashyamvtatti/roberta-fake-news"}
