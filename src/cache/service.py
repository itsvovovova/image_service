from datetime import timedelta
from src.cache.core import current_connection

def create_session(user_id: str, token: str):
    current_connection.set(token, user_id, ex=timedelta(hours=1))

def get_user(session_id: str) -> str:
    return str(current_connection.get(session_id))