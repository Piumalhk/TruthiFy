from fastapi import APIRouter, HTTPException, Depends, status
from ..models import UserCreate, UserLogin, Token, MessageResponse
from ..services import UserService
from ..auth import get_current_active_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Initialize service
user_service = UserService()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        user_id = await user_service.create_user(user_data)
        return MessageResponse(message=f"User {user_data.username} created successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=Token)
async def login_user(user_data: UserLogin):
    """Login user and return access token"""
    user = await user_service.authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await user_service.create_access_token_for_user(user["username"])
    return Token(access_token=access_token, token_type="bearer")

@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_active_user)):
    """Get current user profile with statistics"""
    user_stats = await user_service.get_user_stats(str(current_user["_id"]))
    
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "created_at": current_user["created_at"],
        "is_active": current_user["is_active"],
        "stats": user_stats
    }

@router.post("/logout")
async def logout_user(current_user: dict = Depends(get_current_active_user)):
    """Logout user (client-side token removal)"""
    return MessageResponse(message="Logged out successfully")

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """Get basic current user info"""
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "is_active": current_user["is_active"]
    }
