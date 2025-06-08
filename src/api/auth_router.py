from fastapi import HTTPException
from time import time
from src.config import get_settings
from fastapi import APIRouter
from src.database.schemas import UserRequest
from src.database.service import user_exists, add_user, password_verification
from jwt import encode
auth_router = APIRouter()

@auth_router.post("/register", status_code=201)
async def register_user(userdata: UserRequest):
    add_user(userdata)
    return {"detail": "User created"}

@auth_router.post("/login", status_code=200)
async def login_user(userdata: UserRequest):
    user_exists(userdata.username)
    if password_verification(userdata):
        token = encode(
            {"username": userdata.username, "exp": get_settings().jwt_expire_minutes * 60 + time()},
            get_settings().jwt_secret_key,
            algorithm=get_settings().jwt_algorithm
        )
        return {"token": token}
    raise HTTPException(status_code=401, detail={"detail": "Invalid credentials"})
