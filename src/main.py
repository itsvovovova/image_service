from fastapi import FastAPI
from src.api import router

# Создаем микросервис
app = FastAPI()

# Подключаем роутер из api/router.py
app.include_router(router.current_router)