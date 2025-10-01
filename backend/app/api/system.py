from fastapi import APIRouter, HTTPException
from ..database import get_database, db
import logging
import psutil
import os
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/system", tags=["System & Health"])

@router.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {}
    }
    
    # Check database connection
    try:
        database = get_database()
        if database and db.connected:
            await database.command("ping")
            health_status["services"]["database"] = {
                "status": "connected",
                "type": "MongoDB",
                "database_name": database.name
            }
        else:
            health_status["services"]["database"] = {
                "status": "disconnected",
                "type": "MongoDB"
            }
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["services"]["database"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check AI model
    try:
        from ..model import FakeNewsModel
        model = FakeNewsModel()
        health_status["services"]["ai_model"] = {
            "status": "loaded",
            "model_name": "hamzab/roberta-fake-news-classification",
            "device": str(model.device)
        }
    except Exception as e:
        health_status["services"]["ai_model"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status

@router.get("/status")
async def system_status():
    """Get basic system status"""
    return {
        "api": "TruthiFy API",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "Available in production"
    }

@router.get("/metrics")
async def system_metrics():
    """Get system performance metrics"""
    try:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total if os.name != 'nt' else psutil.disk_usage('C:').total,
                "free": psutil.disk_usage('/').free if os.name != 'nt' else psutil.disk_usage('C:').free,
                "percent": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system metrics")

@router.get("/info")
async def api_info():
    """Get API information and endpoints"""
    return {
        "name": "TruthiFy API",
        "version": "1.0.0",
        "description": "Fake News Detection API with User Management",
        "endpoints": {
            "authentication": "/auth/*",
            "news_analysis": "/news/*",
            "user_history": "/history/*",
            "system": "/system/*"
        },
        "documentation": "/docs",
        "openapi_schema": "/openapi.json"
    }

@router.get("/ping")
async def ping():
    """Simple ping endpoint for monitoring"""
    return {"message": "pong", "timestamp": datetime.utcnow().isoformat()}
