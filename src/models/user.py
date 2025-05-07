from pydantic import BaseModel

class User(BaseModel):
    id: str
    login: str
    password: str
