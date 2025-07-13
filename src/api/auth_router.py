from fastapi import HTTPException, Depends
from time import time

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from fastapi import APIRouter

from src.database.dependencies import get_async_session
from src.database.schemas import UserRequest
from src.database.service import add_user, password_verification
from jwt import encode
from src.cache.service import create_session
auth_router = APIRouter()

@auth_router.post("/register", status_code=201)
async def register_user(userdata: UserRequest, session: AsyncSession = Depends(get_async_session)):
    await add_user(userdata, session)
    return {"detail": "User created"}

@auth_router.post("/login", status_code=200)
async def login_user(userdata: UserRequest, session: AsyncSession = Depends(get_async_session)):
    if password_verification(userdata, session):
        """
        The password verification function also handles
        the case when the login does not exist in the database.
        """
        token = encode(
            {"username": userdata.username, "exp": get_settings().jwt_expire_minutes * 60 + time()},
            get_settings().jwt_secret_key,
            algorithm=get_settings().jwt_algorithm
        )
        await create_session(userdata.username, token)
        return {"token": token}
    raise HTTPException(status_code=401, detail={"detail": "Invalid credentials"})
