from src.models.user import User

class UserStorage:
    def __init__(self):
        self.data: dict[str, User] = {}

    def get_password(self, user_id: str) -> str:
        return self.data[user_id].password

# Создаем новое хранилище
users_storage = UserStorage()

