import base64
import uuid
from time import time
from logging import getLogger
from fastapi import APIRouter, Header, HTTPException
from starlette.concurrency import run_in_threadpool
from src.consumers.send_message import send_to_rabbitmq
from src.database.service import add_task, task_exist, get_result, get_status, verification_task
from src.database.schemas import TaskRequest, TaskCreateRequest
from fastapi.responses import StreamingResponse
from io import BytesIO
from src.authorization.authorization import get_token
from src.metrics.metrics import WORK_TIME, FILTERS_USED

logger = getLogger(__name__)

current_router = APIRouter()

@current_router.post("/task", status_code=201)
async def create(req: TaskCreateRequest, authorization: str = Header(...)):
    # 1. Декодируем base64 в байты
    try:
        image_bytes = base64.b64decode(req.photo)
    except Exception:
        raise HTTPException(status_code=400, detail={"detail": "Invalid base64 in `photo` field"})
    start_time = time()
    # 2. Отправляем задачу в RabbitMQ и ждём результата
    try:
        result_bytes = await run_in_threadpool(send_to_rabbitmq, image_bytes, req.filter)
    except Exception as err:
        raise HTTPException(status_code=500, detail={"detail": f"Processing error: {err}"})

    end_time = time() - start_time
    WORK_TIME.observe(end_time)
    FILTERS_USED.labels(filter=req.filter).inc()
    try:
        token = authorization.split(maxsplit=1)[1]
    except:
        raise HTTPException(status_code=400, detail={"detail": "Assert error"})
    # 3. Сохраняем задачу в хранилище
    try:
        task_uuid = str(uuid.uuid4())
        add_task(TaskRequest(task_id=task_uuid, user_token=token, photo=image_bytes, result=result_bytes, filter=req.filter, status="ready"))
    except KeyError:
        raise HTTPException(status_code=400, detail="Task already exist")
    # 4. Возвращаем идентификатор задачи
    return {"task_id": task_uuid}

@current_router.get("/status/{task_id}")
async def get_status_task(task_id: str, authorization: str = Header(...)):
    token = get_token(authorization)
    if not task_exist(task_id):
        raise HTTPException(status_code=404, detail="Task not exist")
    if not verification_task(task_id, token):
        raise HTTPException(status_code=403, detail={"detail": "Insufficient user rights"})
    task_status = get_status(task_id)
    return {"status": task_status}

@current_router.get("/result/{task_id}")
async def get_result_task(task_id: str, authorization: str = Header(...)):
    token = get_token(authorization)
    if not task_exist(task_id):
        raise HTTPException(status_code=404, detail="Task not exist")
    if not verification_task(task_id, token):
        raise HTTPException(status_code=403, detail={"detail": "Insufficient user rights"})
    task_result = BytesIO(get_result(task_id))
    logger.info("The result appeared on the page")
    return StreamingResponse(task_result, media_type="image/png")

