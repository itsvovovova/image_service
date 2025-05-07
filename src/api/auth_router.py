from fastapi import APIRouter
from src.models.user import User
from src.services.storage import TaskStorage

auth_router = APIRouter()

@auth_router.post("/register, {user_data}")
async def register_user(user_data: User):
    TaskStorage

