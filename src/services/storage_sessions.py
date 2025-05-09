from src.models.session import Session

class SessionStorage:
    def __init__(self):
        self.data: dict[str, Session] = {}

    def get_user_id(self, session_id: str) -> str:
        return self.data[session_id].user_id

# Создаем новое хранилище
session_storage = SessionStorage()

