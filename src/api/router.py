import base64
import uuid
from time import time
from logging import getLogger
from requests import get
from fastapi import APIRouter, Header, HTTPException
from starlette.concurrency import run_in_threadpool
from src.consumers.send_message import send_to_rabbitmq
from src.database.service import add_task, task_exist, get_result, get_status, verification_task
from src.database.schemas import TaskRequest, TaskCreateRequest
from fastapi.responses import StreamingResponse
from io import BytesIO
from src.metrics.metrics import WORK_TIME, FILTERS_USED

logger = getLogger(__name__)

current_router = APIRouter()

@current_router.post("/task", status_code=201)
async def create(req: TaskCreateRequest, authorization: str = Header(...)):
    """
    The problem is that storing photos in a database
    is quite a resource-intensive process,
    so have to work with bytes.
    """
    url = str(req.photo)
    response = get(url)
    image_bytes = response.content
    # The photo processing time starts with sending the photo to RabbitMQ
    start_time = time()
    try:
        result_bytes = await run_in_threadpool(send_to_rabbitmq, image_bytes, req.filter)
    except Exception as err:
        raise HTTPException(status_code=500, detail={"detail": f"Processing error: {err}"})
    end_time = time() - start_time
    WORK_TIME.observe(end_time)
    # The filter used is also saved here
    FILTERS_USED.labels(filter=req.filter).inc()
    """
    There is no validation here because it has already been
    completed successfully in middleware authorization
    """
    token = authorization.split(maxsplit=1)[1]
    task_uuid = str(uuid.uuid4())
    """
    An important point. You may notice that here
    the photo is immediately placed in the database
    with the result. This is due to the fact that the
    photo must be processed quickly enough, and there
    is no need to perform unnecessary actions with the database.
    """
    add_task(TaskRequest(
        task_id=task_uuid, user_token=token,
        photo=image_bytes, result=result_bytes,
        filter=req.filter, status="ready"))
    return {"task_id": task_uuid}

@current_router.get("/status/{task_id}")
async def get_status_task(task_id: str, authorization: str = Header(...)):
    """
    There is no validation here because it has already been
    completed successfully in middleware authorization
    """
    token = authorization.split(maxsplit=1)[1]
    if not task_exist(task_id):
        raise HTTPException(status_code=404, detail="Task not exist")
    if not verification_task(task_id, token):
        raise HTTPException(status_code=403, detail={"detail": "Insufficient user rights"})
    task_status = get_status(task_id)
    return {"status": task_status}

@current_router.get("/result/{task_id}")
async def get_result_task(task_id: str, authorization: str = Header(...)):
    """
    There is no validation here because it has already been
    completed successfully in middleware authorization
    """
    token = authorization.split(maxsplit=1)[1]
    if not task_exist(task_id):
        raise HTTPException(status_code=404, detail="Task not exist")
    if not verification_task(task_id, token):
        raise HTTPException(status_code=403, detail={"detail": "Insufficient user rights"})
    task_result = BytesIO(get_result(task_id))
    logger.info("The result appeared on the page")
    return StreamingResponse(task_result, media_type="image/jpeg")

