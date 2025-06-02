import base64
import uuid

from fastapi import APIRouter, Header, HTTPException
from starlette.concurrency import run_in_threadpool
from src.consumers.send_message import send_to_rabbitmq
from src.database.service import add_task, task_exist
from src.database.schemas import TaskRequest, TaskCreateRequest
from src.database.service import get_result, get_status
current_router = APIRouter()

@current_router.post("/task", status_code=201)
async def create(req: TaskCreateRequest, authorization: str = Header(...)):
    # 1. Декодируем base64 в байты
    try:
        image_bytes = base64.b64decode(req.photo)
    except Exception:
        raise HTTPException(status_code=400, detail={"detail": "Invalid base64 in `photo` field"})
    # 2. Отправляем задачу в RabbitMQ и ждём результата
    try:
        result_bytes = await run_in_threadpool(send_to_rabbitmq, image_bytes, req.filter)
    except Exception as err:
        raise HTTPException(status_code=500, detail={"detail": f"Processing error: {err}"})
    try:
        token = authorization.split(maxsplit=1)[1]
    except:
        raise HTTPException(status_code=400, detail={"detail": "Assert error"})
    # 3. Сохраняем задачу в хранилище
    try:
        task_uuid = str(uuid.uuid4())
        add_task(TaskRequest(task_id=task_uuid, photo=image_bytes, result=result_bytes, filter=req.filter, status="ready"))
    except KeyError:
        raise HTTPException(status_code=400, detail="Task already exist")
    # 4. Возвращаем идентификатор задачи
    return {"task_id": task_uuid} # все-таки нужно taskid добавить
@current_router.get("/status/{task_id}")
async def get_status_task(task_id: str, authorization: str = Header(...)):
    if not task_exist(task_id):
        raise HTTPException(status_code=404, detail="Task not exist")
    task_status = get_status(task_id)
    return {"status": task_status}

@current_router.get("/result/{task_id}")
async def get_result_task(task_id: str, authorization: str = Header(...)):
    if not task_exist(task_id):
        raise HTTPException(status_code=404, detail="Task not exist")
    task_result = get_result(task_id)
    return {"result": task_result}

