# history.py
from fastapi import APIRouter, Depends
from auth import get_current_user
from database import history_collection
from schemas import HistoryItem
from datetime import datetime

router = APIRouter(prefix="/api/v1/history", tags=["history"])

@router.get("/")
async def get_history(current_user=Depends(get_current_user)):
    items = await history_collection.find({"user_id": current_user["username"]}).to_list(100)
    return {"history": items}

@router.get("/stats")
async def get_stats(current_user=Depends(get_current_user)):
    items = await history_collection.find({"user_id": current_user["username"]}).to_list(1000)
    total = len(items)
    fake = sum(1 for i in items if i["prediction"] == "FAKE")
    real = sum(1 for i in items if i["prediction"] == "REAL")
    return {"total_analyses": total, "fake_count": fake, "real_count": real}

@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: str, current_user=Depends(get_current_user)):
    result = await history_collection.delete_one({"_id": analysis_id, "user_id": current_user["username"]})
    return {"deleted_count": result.deleted_count}

@router.delete("/")
async def clear_history(current_user=Depends(get_current_user)):
    result = await history_collection.delete_many({"user_id": current_user["username"]})
    return {"deleted_count": result.deleted_count}
