from asyncio import sleep
from uuid import UUID
from fastapi import APIRouter, Body, File
from starlette.responses import JSONResponse
from src.models.task import Task
from src.services.storage import new_storage

current_router = APIRouter()

@current_router.post("/task", status_code=201)
async def create(current_task: bytes = File(...)):
    await sleep(5)
    current_uuid = new_storage.add(Task(result="garbage.jpg", status="ready", data=current_task))
    return {"task_id": str(current_uuid)}

@current_router.get("/status/{task_id}")
async def get_status(task_id: str):
    try:
        current_id = UUID(task_id)
    except ValueError:
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    if current_id not in new_storage._data:
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return {"status": new_storage._data[current_id].status}

@current_router.get("/result/{task_id}")
async def get_result(task_id: str):
    try:
        id = UUID(task_id)
    except ValueError:
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    if id not in new_storage._data:
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return {"result": new_storage._data[id].result}
