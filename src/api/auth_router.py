import os
from time import time

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.models.session import Session
from src.models.user import User
from src.services.storage_sessions import session_storage
from src.services.storage_users import users_storage
from passlib.hash import bcrypt
import jwt

auth_router = APIRouter()

@auth_router.post("/register")
async def register_user(userdata: User):
    if userdata.username in users_storage.data:
        return JSONResponse(status_code=400, content={"detail": "User already exists"})
    password_hash = bcrypt.hash(userdata.password)
    users_storage.data[userdata.username] = User(username=userdata.username, password=password_hash)
    return JSONResponse(status_code=201, content={"detail": "User created"})

@auth_router.post("/login", status_code=200)
async def login_user(userdata: User):
    if userdata.username not in users_storage.data:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
    current_user = users_storage.data[userdata.username]
    max_time = 10 ** 5
    if bcrypt.verify(userdata.password, current_user.password):
        token = jwt.encode(
            {"username": userdata.username, "exp": max_time + time()},
            "KEY",
            algorithm="HS256"
        )
        session_storage.data[token] = Session(user_id=userdata.username, session_id=token)
        return {"token": token}
    return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
