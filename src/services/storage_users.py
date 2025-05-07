from src.models.user import User
from pydantic import BaseModel


class UserStorage(BaseModel):

    data: dict[User, str]

    def get_password(self, user: User) -> str:
        return self[User]


# Создаем новое хранилище
users_storage = UserStorage()

