from fastapi import FastAPI
from src.api import router, auth_router
from src.authorization.authorization import JWTAuthMiddleware
from src.database.core import engine, Base

# Создаем микросервис
app = FastAPI()

app.add_middleware(JWTAuthMiddleware)

# Подключаем роутер из api/router.py
app.include_router(router.current_router)
app.include_router(auth_router.auth_router)

# Создает таблицы, если их нет
Base.metadata.create_all(bind=engine)