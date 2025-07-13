import asyncio
import base64
import json
from aio_pika import connect_robust, Message, DeliveryMode

from src.consumers.image_processor.filter_photo import filter_photo
from src.config import get_settings
from logging import getLogger

logger = getLogger(__name__)

"""
Listens to the task_queue queue,
processes images on request,
sends the result back via reply_to,
and confirms receipt
"""

async def main():
    settings = get_settings()
    connection = await connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('task_queue', durable=True)
        logger.info("Consumer connected to RabbitMQ")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    current_dict = json.loads(message.body.decode())

                    photo_bytes = base64.b64decode(current_dict["photo"])
                    result = filter_photo(photo_bytes, current_dict["filter"])

                    result_b64 = base64.b64encode(result).decode('utf-8')
                    response = json.dumps({"result": result_b64}).encode()

                    if message.reply_to:
                        await channel.default_exchange.publish(
                            Message(
                                response,
                                correlation_id=message.correlation_id,
                                delivery_mode=DeliveryMode.PERSISTENT,
                            ),
                            routing_key=message.reply_to
                        )
                        logger.info("The photo was sent successfully")

if __name__ == "__main__":
    asyncio.run(main())
