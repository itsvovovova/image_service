from uuid import UUID
from pydantic import BaseModel

# Класс задачи
class Task(BaseModel):
    photo: bytes
    filter: str = "None"
    status: str
    result: bytes


# Response-классы
class TaskCreate(BaseModel):
    task_uuid: UUID

class StatusResponse(BaseModel):
    status: str

class ResultResponse(BaseModel):
    result: str