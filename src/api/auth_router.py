from fastapi import APIRouter
from pydantic.v1 import UUID4

from src.models.user import User
from src.services.storage import TaskStorage
from src.services.storage_users import users_storage
from passlib.hash import bcrypt
from uuid import uuid4, UUID

auth_router = APIRouter()

@auth_router.post("/register, {user_data}")
async def register_user(user_data: User) -> None:
    if user_data.login in users_storage:
        print("The user is already logged in")
    else:
        password = bcrypt.hash(user_data.password)
        users_storage[user_data.login] = password

@auth_router.post("/login, {user_data}")
async def login_user(user_data: User) -> UUID:
    password = bcrypt.hash(user_data.password)
    if user_data.login in users_storage and user_data.password == password:
        token = uuid4()
        users_storage.data[user_data] = token
        return token


