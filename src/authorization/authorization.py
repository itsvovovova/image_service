import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from logging import getLogger
from starlette.responses import JSONResponse
from src.config import get_settings

logger = getLogger(__name__)

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(("/login", "/register", "/metrics", "/docs", "redoc", "/openapi.json")):
            return await call_next(request)
        auth = request.headers.get("authorization")
        if not auth or not auth.startswith("Bearer "):
            logger.info("The token does not start with 'Bearer '")
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
        token = auth.split(maxsplit=1)[1]
        try:
            payload = jwt.decode(token, get_settings().jwt_secret_key, algorithms=get_settings().jwt_algorithm)
        except:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        request.state.user_id = payload.get("username")
        return await call_next(request)




