from datetime import datetime
from .auth import get_password_hash, verify_password, create_access_token

class UserService:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user_data):
        hashed_password = get_password_hash(user_data.password)
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "password": hashed_password,
            "full_name": user_data.full_name,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        result = await self.db.users.insert_one(user_dict)
        return str(result.inserted_id)

    async def authenticate_user(self, username: str, password: str):
        user = await self.db.users.find_one({"username": username})
        if user and verify_password(password, user["password"]):
            return user
        return None

    async def create_access_token_for_user(self, username: str):
        return create_access_token({"sub": username})

    async def get_user_stats(self, user_id: str):
        # Example placeholder
        return {"logins": 10, "actions": 25}
