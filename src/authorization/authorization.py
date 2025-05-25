import os

import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # логим каждый запрос
        print(f"[MW] PATH={request.url.path!r}, AUTH={request.headers.get('authorization')!r}")

        if request.url.path.startswith(("/login", "/register")):
            return await call_next(request)

        auth = request.headers.get("authorization")
        if not auth or not auth.startswith("Bearer "):
            print("  → Missing or malformed Bearer header")
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        token = auth.split(maxsplit=1)[1]
        try:
            payload = jwt.decode(token, "KEY", algorithms=["HS256"])
            print("  → JWT payload:", payload)
        except Exception as e:
            print("  → JWT decode failed:", e)
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        request.state.user_id = payload.get("username")
        return await call_next(request)




