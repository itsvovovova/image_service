from datetime import timedelta
from src.cache.core import current_connection

async def create_session(user_id: str, token: str):
    await current_connection.set(token, user_id, ex=timedelta(hours=1))

async def get_user(session_id: str) -> str:
    value = await current_connection.get(session_id)
    return str(value)
