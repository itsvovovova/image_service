import uuid
from time import time
from logging import getLogger

import httpx
from fastapi import APIRouter, Header, HTTPException, Depends, FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO

from src.consumers.send_message import send_to_rabbitmq
from src.database.core import async_engine
from src.database.models import Base
from src.database.service import (
    add_task, task_exist, get_result, get_status, verification_task
)
from src.database.schemas import TaskRequest, TaskCreateRequest
from src.cache.service import get_user
from src.metrics.metrics import WORK_TIME, FILTERS_USED
from src.database.dependencies import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

logger = getLogger(__name__)

current_router = APIRouter()

async def lifespan(app: FastAPI):
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

@current_router.post("/task", status_code=201)
async def create(
    req: TaskCreateRequest,
    authorization: str = Header(...),
    session: AsyncSession = Depends(get_async_session)
):
    """
    The problem is that storing photos in a database
    is quite a resource-intensive process,
    so have to work with bytes.
    """
    url = str(req.photo)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        image_bytes = response.content
    # The photo processing time starts with sending the photo to RabbitMQ
    start_time = time()
    try:
        result_bytes = await send_to_rabbitmq(image_bytes, req.filter)
    except Exception as err:
        raise HTTPException(status_code=500, detail={"detail": f"Processing error: {err}"})
    end_time = time() - start_time
    WORK_TIME.observe(end_time)

    # The filter used is also saved here
    FILTERS_USED.labels(filter=req.filter).inc()

    token = authorization.split(maxsplit=1)[1]
    user = await get_user(token)
    task_uuid = str(uuid.uuid4())
    await add_task(TaskRequest(
        task_id=task_uuid,
        username=user,
        photo=image_bytes,
        result=result_bytes,
        filter=req.filter,
        status="ready"
    ), session)
    return {"task_id": task_uuid}

@current_router.get("/status/{task_id}")
async def get_status_task(
    task_id: str,
    authorization: str = Header(...),
    session: AsyncSession = Depends(get_async_session)
):
    token = authorization.split(maxsplit=1)[1]
    if not await task_exist(task_id, session):
        raise HTTPException(status_code=404, detail="Task not exist")
    if not await verification_task(task_id, token, session):
        raise HTTPException(status_code=403, detail={"detail": "Insufficient user rights"})
    task_status = await get_status(task_id, session)
    return {"status": task_status}

@current_router.get("/result/{task_id}")
async def get_result_task(
    task_id: str,
    authorization: str = Header(...),
    session: AsyncSession = Depends(get_async_session)
):
    token = authorization.split(maxsplit=1)[1]
    if not await task_exist(task_id, session):
        raise HTTPException(status_code=404, detail="Task not exist")
    if not await verification_task(task_id, token, session):
        raise HTTPException(status_code=403, detail={"detail": "Insufficient user rights"})
    result_bytes = await get_result(task_id, session)
    task_result = BytesIO(result_bytes)
    logger.info("The result appeared on the page")
    return StreamingResponse(task_result, media_type="image/jpeg")
