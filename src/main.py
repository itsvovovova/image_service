from src import logger
from fastapi import FastAPI
from src.api import router, auth_router
from src.authorization.authorization import JWTAuthMiddleware
from src.database.core import engine
from src.database.models import Base
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.add_middleware(JWTAuthMiddleware)

app.include_router(router.current_router)
app.include_router(auth_router.auth_router)

Base.metadata.create_all(bind=engine)