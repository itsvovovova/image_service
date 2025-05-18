import base64
from uuid import UUID
from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool
from starlette.responses import JSONResponse
from src.models.task import Task, TaskRequest
from src.services.storage import new_storage
from src.consumers.send_message import send_to_rabbitmq

current_router = APIRouter()

@current_router.post("/task", status_code=201)
async def create(req: TaskRequest):
    # 1. Декодируем base64 в байты
    try:
        image_bytes = base64.b64decode(req.photo)
    except Exception:
        return JSONResponse(status_code=400, content={"detail": "Invalid base64 in `photo` field"})
    # 2. Отправляем задачу в RabbitMQ и ждём результата
    try:
        result_bytes = await run_in_threadpool(send_to_rabbitmq, image_bytes, req.filter)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Processing error: {e}"})
    # 3. Сохраняем задачу в хранилище
    task = Task(status="ready", photo=image_bytes, result=result_bytes)
    task_id = new_storage.add(task)

    # 4. Возвращаем идентификатор задачи
    return JSONResponse(status_code=201, content={"task_id": str(task_id)})


@current_router.get("/status/{task_id}")
async def get_status(task_id: str):
    try:
        current_id = UUID(task_id)
    except ValueError:
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    if current_id not in new_storage.data:
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return {"status": new_storage.data[current_id].status}

@current_router.get("/result/{task_id}")
async def get_result(task_id: str):
    try:
        uid = UUID(task_id)
    except ValueError:
        return JSONResponse("Error", 404)
    if uid not in new_storage.data:
        return JSONResponse(content="Not found", status_code=404)
    raw = new_storage.data[uid].result
    encoded = base64.b64encode(raw).decode("utf-8")
    return {"result": encoded}
