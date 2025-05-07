from fastapi import FastAPI
from src.api import router
from src.authorization.authorization import JWTAuthMiddleware

# Создаем микросервис
app = FastAPI()

app.add_middleware(JWTAuthMiddleware)

# Подключаем роутер из api/router.py
app.include_router(router.current_router)