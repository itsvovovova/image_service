from logging import getLogger
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import User, Task
from src.database.schemas import UserRequest, TaskRequest
from src.cache.service import get_user

logger = getLogger(__name__)

async def password_verification(user: UserRequest, session: AsyncSession) -> bool:
    current_password = user.password
    result = await session.execute(
        select(User.password).where(User.username == user.username)
    )
    hashed = result.scalar_one_or_none()
    if not hashed or not bcrypt.verify(current_password, hashed):
        logger.warning("Incorrect password for user")
        raise HTTPException(status_code=401, detail="Incorrect password")
    logger.debug("Password verified for user")
    return True

async def add_user(user: UserRequest, session: AsyncSession):
    result = await session.execute(
        select(User.username).where(User.username == user.username)
    )
    if result.scalar_one_or_none():
        logger.warning("User already exists")
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = bcrypt.hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    session.add(new_user)
    await session.commit()
    logger.info("The user  has been added to database")

async def user_exists(login: str, session: AsyncSession) -> str:
    result = await session.execute(
        select(User.password).where(User.username == login)
    )
    current_user = result.scalar_one_or_none()
    if not current_user:
        logger.warning("Current user  not found", login)
        raise HTTPException(status_code=404, detail="Current user not found")
    logger.info("User exists")
    return current_user

async def add_task(task: TaskRequest, session: AsyncSession):
    result = await session.execute(
        select(Task.id).where(Task.id == task.task_id)
    )
    if result.scalar_one_or_none():
        logger.warning("Task already exist")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already exists")

    current_object = Task(
        username=task.username,
        id=task.task_id,
        photo=task.photo,
        filter=task.filter,
        result=task.result,
        status="ready"
    )
    session.add(current_object)
    await session.commit()
    logger.info("Task added")

async def task_exist(task_id: str, session: AsyncSession) -> bool:
    result = await session.execute(
        select(Task.id).where(Task.id == task_id)
    )
    exists = result.scalar_one_or_none() is not None
    logger.info("Task exists")
    return exists

async def get_status(task_id: str, session: AsyncSession) -> str:
    if not await task_exist(task_id, session):
        logger.warning("Task not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not exist")
    result = await session.execute(
        select(Task.status).where(Task.id == task_id)
    )
    status_value = result.scalar_one()
    logger.info("The user got the photo status for task")
    return status_value

async def get_result(task_id: str, session: AsyncSession) -> bytes:
    if not await task_exist(task_id, session):
        logger.warning("Task  not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not exist")
    result = await session.execute(
        select(Task.result).where(Task.id == task_id)
    )
    data = result.scalar_one()
    logger.info("The user received the photo for task")
    return data

async def verification_task(task_id: str, token: str, session: AsyncSession) -> bool:
    result = await session.execute(
        select(Task.username).where(Task.id == task_id)
    )
    owner = result.scalar_one_or_none()
    if not owner or owner != await get_user(token):
        logger.info("Insufficient user rights for task")
        return False
    logger.info("The photo of task  belongs to user")
    return True












