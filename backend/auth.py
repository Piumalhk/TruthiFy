# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
import os
import hashlib
from datetime import datetime, timedelta
from database import users_collection

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Password hashing

def hash_password(password: str) -> str:
    """
    Securely hash the password by pre-hashing with SHA-256 before bcrypt.
    """
    # Step 1: Encode and hash password using SHA-256 (shortens long inputs)
    sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # Step 2: Bcrypt-hash the SHA result
    return pwd_context.hash(sha)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a stored bcrypt hash.
    """
    sha = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(sha, hashed_password)

# JWT creation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await users_collection.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # RETURN CLEAN USER OBJECT
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
