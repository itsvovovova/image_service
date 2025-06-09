import json
import uuid
import base64
import pika
from src.config import get_settings
from logging import getLogger

logger = getLogger(__name__)

def send_to_rabbitmq(image_bytes: bytes, filter_name: str) -> bytes:
    """
    This function takes a photo and a filter as input,
    sends a message to the RabbitMQ intermediary,
    waits for a response, and returns the result of processing the photo.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=get_settings().rabbitmq_host,
            port=get_settings().rabbitmq_port)
    )

    channel = connection.channel()
    # Temporary response queue
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue
    # To compare a request and a response
    corr_id = str(uuid.uuid4())
    encoded_image = base64.b64encode(image_bytes).decode()

    response = None

    # Needed to get a response
    def on_response(ch, method, props, body):
        nonlocal response
        if props.correlation_id == corr_id:
            response = json.loads(body.decode())["result"]
            ch.stop_consuming()

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True
    )

    message = json.dumps({
        "photo": encoded_image,
        "filter": filter_name
    })

    # Sending a photo
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id
        ),
        body=message.encode()
    )

    logger.info("The photo has been sent successfully, waiting for a response.")

    # Waiting for a response
    channel.start_consuming()

    decoded_result = base64.b64decode(response)
    logger.info("The modified photo was received")
    connection.close()
    return decoded_result
