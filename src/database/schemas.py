from pydantic import BaseModel, HttpUrl

class TaskCreateRequest(BaseModel):
    photo: HttpUrl
    filter: str

class TaskRequest(BaseModel):
    task_id: str
    user_token: str
    photo: bytes
    filter: str = "negative"
    status: str = "in progress"
    result: bytes = bytes()

class UserRequest(BaseModel):
    username: str
    password: str

