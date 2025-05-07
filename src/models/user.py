from pydantic import BaseModel
from pydantic.v1 import UUID4


class User(BaseModel):
    id: UUID4
    login: str
    password: str
