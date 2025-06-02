import uuid
from datetime import timedelta
from src.cache.core import current_connection

def create_session(user_id: str) -> str:
    session_id = str(uuid.uuid4())
    current_connection.set(session_id, user_id, ex=timedelta(hours=1))
    return session_id

def get_user(session_id: str) -> str:
    return current_connection.get(session_id)