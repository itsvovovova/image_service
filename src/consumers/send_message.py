import json
import uuid
import base64
import asyncio
from aio_pika import connect_robust, Message, DeliveryMode  # ← замена pika на aio-pika
from src.config import get_settings
from logging import getLogger

logger = getLogger(__name__)

async def send_to_rabbitmq(image_bytes: bytes, filter_name: str) -> bytes:
    """
    This function takes a photo and a filter as input,
    sends a message to the RabbitMQ intermediary,
    waits for a response, and returns the result of processing the photo.
    """
    settings = get_settings()
    connection = await connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )

    async with connection:
        channel = await connection.channel()
        # Temporary response queue
        callback_queue = await channel.declare_queue(exclusive=True)
        # To compare a request and a response
        corr_id = str(uuid.uuid4())
        encoded_image = base64.b64encode(image_bytes).decode()

        response_future = asyncio.get_event_loop().create_future()

        # Needed to get a response
        async def on_response(message):
            if message.correlation_id == corr_id:
                body = json.loads(message.body.decode())
                response_future.set_result(body["result"])
            await message.ack()

        await callback_queue.consume(on_response)  # ← await

        message = json.dumps({
            "photo": encoded_image,
            "filter": filter_name
        }).encode()

        # Sending a photo
        msg = Message(
            message,
            correlation_id=corr_id,
            reply_to=callback_queue.name,
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await channel.default_exchange.publish(msg, routing_key="task_queue")
        logger.info("The photo has been sent successfully, waiting for a response.")

        # Waiting for a response
        result_b64 = await asyncio.wait_for(response_future, timeout=30)
        decoded_result = base64.b64decode(result_b64)
        logger.info("The modified photo was received")

        return decoded_result
