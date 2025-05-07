from asyncio import sleep
from fastapi import APIRouter
from src.models.task import Task, ResultResponse, StatusResponse, TaskCreate
from src.services.storage import new_storage

# Создаем роутер
current_router = APIRouter()

# Получаем результат
@current_router.get("/get_result/{task_id}", response_model=ResultResponse)
async def get_result(task_id: str) -> ResultResponse:
    return ResultResponse(result=new_storage[task_id].result)

# Получаем статус
@current_router.get("/get_status/{task_id}", response_model=StatusResponse)
async def get_status(task_uuid: str) -> StatusResponse:
    return StatusResponse(status=new_storage[task_uuid].status)

# Создаем объект класса
@current_router.post("/task")
async def create() -> TaskCreate:
    await sleep(5)
    task_id = new_storage.add(Task(result="garbage.jpg", status="ready", data=''))
    return task_id



