from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import connect_to_mongo, close_mongo_connection
from .api.routes import api_router
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
    allow_origins=["http://localhost:3000", 
                   "http://127.0.0.1:3000",
                   "http://localhost:5173",   #
                  "http://127.0.0.1:5173" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Legacy endpoint for backward compatibility
@app.post("/predict")
async def legacy_predict(request: dict):
    """Legacy prediction endpoint - redirects to new API structure"""
    from .api.news import analyze_news_anonymous
    from .models import TextRequest
    
    try:
        text_request = TextRequest(text=request.get("text", ""))
        return await analyze_news_anonymous(text_request)
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {
        "message": "TruthiFy API is running", 
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1"
    }