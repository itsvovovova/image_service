from uuid import UUID
from pydantic import BaseModel

# Класс задачи
class Task(BaseModel):
    user: str
    photo: bytes
    filter: str = "None"
    status: str
    result: bytes


# Response-классы

class TaskRequest(BaseModel):
    photo: str
    filter: str

# class TaskCreate(BaseModel):
#     task_uuid: UUID
#
# class StatusResponse(BaseModel):
#     status: str
#
# class ResultResponse(BaseModel):
#     result: str

# class FilterRequest(BaseModel):
#     filter: str