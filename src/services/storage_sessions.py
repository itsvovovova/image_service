from pydantic import BaseModel
from src.models.session import Session

class SessionStorage(BaseModel):

    data: dict[str, Session] # session_id -> session

    def get_user_id(self, session_id: str) -> str:
        return self[session_id].user_id


# Создаем новое хранилище
session_storage = SessionStorage()

