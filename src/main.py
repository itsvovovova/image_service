from fastapi import FastAPI
from src.api import router, auth_router
from src.authorization.authorization import JWTAuthMiddleware
from src.database.core import engine, Base
from prometheus_fastapi_instrumentator import Instrumentator

# Создаем микросервис
app = FastAPI()

# Создаем метрики
Instrumentator().instrument(app).expose(app)

app.add_middleware(JWTAuthMiddleware)

# Подключаем роутер из api/router.py
app.include_router(router.current_router)
app.include_router(auth_router.auth_router)

# Создает таблицы, если их нет
Base.metadata.create_all(bind=engine)