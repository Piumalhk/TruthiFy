from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.hash import argon2
from jose import JWTError, jwt
from .database import get_database
from .models import TokenData
import os
from dotenv import load_dotenv

load_dotenv()

# Config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY or SECRET_KEY == "your-secret-key-here-change-this-in-production-2024-secure-key":
    raise ValueError("SECRET_KEY must be set to a secure value in .env file")

security = HTTPBearer()


# ---------------------------
# Password hashing using Argon2
# ---------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    try:
        return argon2.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    try:
        if not password:
            raise ValueError("Password cannot be empty")
        return argon2.hash(password)
    except Exception as e:
        raise ValueError(f"Password hashing failed: {str(e)}")


# ---------------------------
# JWT token creation and verification
# ---------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    db = get_database()
    user = await db.users.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Get current active user"""
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
