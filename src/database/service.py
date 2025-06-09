from logging import getLogger
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import select
from fastapi import HTTPException
from src.database.models import User, Task
from src.database.core import engine, Session
from src.database.schemas import UserRequest, TaskRequest

logger = getLogger(__name__)

def password_verification(user: UserRequest) -> bool:
    current_password, password = user.password, user_exists(user.username)
    if not bcrypt.verify(current_password, password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    return True

def add_user(user: UserRequest):
    with Session(bind=engine) as current_session:
        with current_session.begin():
            existing_password = current_session.execute(
                select(User.username).where(User.username == user.username)
            ).scalar()
            if existing_password:
                raise HTTPException(status_code=400, detail="User already exists")

            hashed_password = bcrypt.hash(user.password)
            new_user = User(username=user.username, password=hashed_password)
            current_session.add(new_user)
    logger.info("The user has been added in database")

def user_exists(login: str) -> str:
    with Session(bind=engine) as current_session:
        with current_session.begin():
            request = select(User.password).where(User.username == login)
            current_user = current_session.execute(request).scalar()
            if not current_user:
                raise HTTPException(status_code=400, detail="Current user not found")
    logger.info("This user exists")
    return str(current_user)

def add_task(task: TaskRequest):
    if task_exist(task.task_id):
        raise KeyError("Task already exist")
    with Session(bind=engine) as current_session:
        with current_session.begin():
            current_object = Task(user_token=task.user_token, id=task.task_id, photo=task.photo, filter=task.filter, result=task.result, status="ready")
            current_session.add(current_object)
    logger.info("Task added")

def task_exist(task_id: str) -> bool:
    with Session(bind=engine) as current_session:
        with current_session.begin():
            request = select(Task).where(Task.id == task_id)
            if not current_session.execute(request).scalar():
                return False
    logger.info("The user's task has been found")
    return True

def get_status(task_id: str) -> str:
    if not task_exist(task_id):
        raise KeyError("Task not exist")
    with Session(bind=engine) as current_session:
        with current_session.begin():
            request = select(Task.status).where(Task.id == task_id)
            logger.info("The user got the photo status")
            return str(current_session.execute(request).scalar())

def get_result(task_id: str) -> bytes:
    if not task_exist(task_id):
        raise KeyError("Task not exist")
    with Session(bind=engine) as current_session:
        with current_session.begin():
            request = select(Task.result).where(Task.id == task_id)
            logger.info("The user received the photo")
            return current_session.execute(request).scalar()

def verification_task(task_id: str, token: str) -> bool:
    with Session(bind=engine) as current_session:
        with current_session.begin():
            request = select(Task.user_token).where(Task.id == task_id)
            if not current_session.execute(request).scalar() or current_session.execute(request).scalar() != token:
                logger.info("Insufficient user rights")
                return False
            logger.info("The photo of this user was found")
            return True












