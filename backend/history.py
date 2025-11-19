from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user
from database import history_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/api/v1/history", tags=["history"])


# Convert MongoDB document → JSON-safe
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    if "timestamp" in doc:
        doc["timestamp"] = doc["timestamp"].isoformat()
    return doc


@router.get("/")
async def get_history(current_user=Depends(get_current_user)):
    items = await history_collection.find({"user_id": current_user["username"]}).to_list(100)

    # Convert ObjectId + datetime → JSON-friendly
    items = [serialize_doc(item) for item in items]

    return {"history": items}


@router.get("/stats")
async def get_stats(current_user=Depends(get_current_user)):
    items = await history_collection.find({"user_id": current_user["username"]}).to_list(1000)

    total = len(items)
    fake = sum(1 for i in items if i["prediction"] == "FAKE")
    real = sum(1 for i in items if i["prediction"] == "REAL")

    return {
        "total_analyses": total,
        "fake_count": fake,
        "real_count": real
    }


@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: str, current_user=Depends(get_current_user)):
    try:
        oid = ObjectId(analysis_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid analysis ID")

    result = await history_collection.delete_one({
        "_id": oid,
        "user_id": current_user["username"]
    })

    return {"deleted_count": result.deleted_count}


@router.delete("/")
async def clear_history(current_user=Depends(get_current_user)):
    result = await history_collection.delete_many({"user_id": current_user["username"]})
    return {"deleted_count": result.deleted_count}
