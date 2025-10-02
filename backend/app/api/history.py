from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from ..models import HistoryResponse, MessageResponse, StatsResponse
from ..services import AnalysisService, UserService
from ..auth import get_current_active_user
from ..database import get_database
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["User History"])

# Dependency injection for services
async def get_analysis_service(db = Depends(get_database)):
    return AnalysisService(db)

async def get_user_service(db = Depends(get_database)):
    return UserService(db)

@router.get("/", response_model=HistoryResponse)
async def get_analysis_history(
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    current_user: dict = Depends(get_current_active_user),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """Get user's analysis history with pagination"""
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

@router.get("/stats", response_model=StatsResponse)
async def get_user_analysis_stats(
    current_user: dict = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get user's analysis statistics"""
    try:
        stats = await user_service.get_user_stats(str(current_user["_id"]))
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Failed to fetch stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")

@router.get("/{analysis_id}")
async def get_single_analysis(
    analysis_id: str,
    current_user: dict = Depends(get_current_active_user),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """Get a specific analysis by ID"""
    try:
        analysis = await analysis_service.get_analysis_by_id(analysis_id, str(current_user["_id"]))
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analysis")

@router.delete("/{analysis_id}", response_model=MessageResponse)
async def delete_analysis(
    analysis_id: str, 
    current_user: dict = Depends(get_current_active_user),
    analysis_service: AnalysisService = Depends(get_analysis_service)
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

@router.delete("/", response_model=MessageResponse)
async def clear_all_history(
    current_user: dict = Depends(get_current_active_user),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """Clear all analysis history for the current user"""
    try:
        deleted_count = await analysis_service.clear_user_history(str(current_user["_id"]))
        return MessageResponse(message=f"Cleared {deleted_count} analyses from history")
    except Exception as e:
        logger.error(f"Failed to clear history: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear history")

@router.get("/export/json")
async def export_history_json(
    current_user: dict = Depends(get_current_active_user),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """Export user's complete analysis history as JSON"""
    try:
        history, _ = await analysis_service.get_user_history(
            str(current_user["_id"]), limit=1000, skip=0
        )
        return {
            "user": current_user["username"],
            "export_date": "2024-01-01",  # You can use datetime.now()
            "total_analyses": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Failed to export history: {e}")
        raise HTTPException(status_code=500, detail="Failed to export history")
