from fastapi import APIRouter, HTTPException, Depends, status
from ..models import UserCreate, UserLogin, Token, MessageResponse
from ..services import UserService
from ..auth import get_current_active_user
from ..database import get_database
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Provide UserService via dependency injection
async def get_user_service(db = Depends(get_database)):
    return UserService(db)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def register_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    logger.info(f"Registration attempt for user: {user_data.username}")
    try:
        if not user_data.username or not user_data.email or not user_data.password:
            raise HTTPException(status_code=400, detail="Username, email, and password are required")
        if len(user_data.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        user_id = await user_service.create_user(user_data)
        return MessageResponse(message=f"User {user_data.username} created successfully")
    except HTTPException as e:
        logger.error(f"HTTP error during registration: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=Token)
async def login_user(
    user_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = await user_service.create_access_token_for_user(user["username"])
    return Token(access_token=access_token, token_type="bearer")

@router.get("/profile")
async def get_user_profile(
    current_user: dict = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
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
    return MessageResponse(message="Logged out successfully")

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "is_active": current_user["is_active"]
    }
