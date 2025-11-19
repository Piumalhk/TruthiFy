# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model.fake_news_model import load_model
from auth import hash_password, verify_password, create_access_token, get_current_user
from database import users_collection, history_collection
from schemas import UserCreate, UserLogin, Token, HistoryItem, AnalyzeRequest
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from history import router as history_router
from fastapi import Depends

app = FastAPI(title="Truthify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load HF model once
pipe = load_model()

# Include history router
app.include_router(history_router)

# ----------------- Auth Endpoints -----------------
@app.post("/api/v1/auth/register")
async def register(user: UserCreate):
    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    await users_collection.insert_one({"username": user.username, "email": user.email, "password": hashed})

    return {"message": "User registered"}

from schemas import UserLogin

@app.post("/api/v1/auth/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/test-db")
async def test_db():
    user_count = await users_collection.count_documents({})
    return {"message": "MongoDB connected successfully!", "total_users": user_count}

@app.get("/api/v1/auth/me")
async def get_me(current_user=Depends(get_current_user)):
    return {"username": current_user["username"]}

# ----------------- Fake News Analysis Endpoint -----------------
@app.post("/api/v1/analyze")
async def analyze_news(request: AnalyzeRequest, current_user=Depends(get_current_user)):
    result = pipe(request.text)[0]
    label = result["label"]
    confidence = round(result["score"], 3)
    timestamp = datetime.utcnow()

    # Calculate probabilities for both REAL and FAKE
    if label == "FAKE":
        fake_prob = confidence
        real_prob = 1 - confidence
    else:
        real_prob = confidence
        fake_prob = 1 - confidence    # Save to history
    await history_collection.insert_one({
        "user_id": current_user["username"],
        "text": request.text,
        "prediction": label,
        "confidence": confidence,
        "timestamp": timestamp
    })

    return {
        "prediction": label,
        "confidence": confidence,
        "probabilities": {
            "REAL": round(real_prob, 3),
            "FAKE": round(fake_prob, 3)
        }
    }

