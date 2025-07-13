from fastapi import FastAPI
from src.api import router, auth_router
from src.authorization.authorization import JWTAuthMiddleware
from src.database.core import async_engine
from src.database.models import Base
from prometheus_fastapi_instrumentator import Instrumentator
from src.api.router import lifespan

app = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

app.add_middleware(JWTAuthMiddleware)

app.include_router(router.current_router)
app.include_router(auth_router.auth_router)