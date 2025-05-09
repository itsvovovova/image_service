from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.models.session import Session
from src.models.user import User
from src.services.storage_sessions import session_storage
from src.services.storage_users import users_storage
from passlib.hash import bcrypt
import jwt

auth_router = APIRouter()

@auth_router.post("/register", status_code=201)
async def register_user(user_data: User):
    if user_data.username in users_storage.data:
        return JSONResponse(status_code=400, content={"detail": "User already exists"})
    password_hash = bcrypt.hash(user_data.password)
    users_storage.data[user_data.username] = password_hash

@auth_router.post("/login", status_code=200)
async def login_user(user_data: User):
    if user_data.username not in users_storage.data:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
    current_password = users_storage.data[user_data.username]
    if bcrypt.verify(user_data.password, current_password):
        token = jwt.encode(
            {"username": user_data.username},
            "SECRET_KEY",
            algorithm="HS256"
        )
        session_storage.data[token] = Session(user_id=user_data.username, session_id=token)
        return {"token": token}
    return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
