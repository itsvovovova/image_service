import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Пропускаем /login, /register
        if request.url.path.startswith(("/login", "/register")):
            return await call_next(request)

        # Получаем токен из заголовка
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        token = auth.split()[1]

        try:
            payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
            user_id = payload.get("username")
            if user_id is None:
                print("Invalid token")
        except:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        # Сохраняем user_id в request.state, чтобы использовать в ручках
        request.state.user_id = user_id

        # Продолжаем обработку запроса
        return await call_next(request)



