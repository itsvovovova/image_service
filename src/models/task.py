from uuid import UUID
from pydantic import BaseModel

# Класс задачи
class Task(BaseModel):
    result: str
    status: str
    data: bytes

# Response-классы
class TaskCreate(BaseModel):
    task_uuid: UUID

class StatusResponse(BaseModel):
    status: str

class ResultResponse(BaseModel):
    result: str