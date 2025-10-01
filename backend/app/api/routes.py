from fastapi import APIRouter
from .auth import router as auth_router
from .news import router as news_router
from .history import router as history_router
from .system import router as system_router

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include all sub-routers
api_router.include_router(auth_router)
api_router.include_router(news_router)
api_router.include_router(history_router)
api_router.include_router(system_router)

# You can also add global API middleware or dependencies here
__all__ = ["api_router"]
