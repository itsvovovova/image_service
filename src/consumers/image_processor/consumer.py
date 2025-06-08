import base64
import json
from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika import PlainCredentials
from pika.spec import BasicProperties
from src.consumers.image_processor.filter_photo import filter_photo
from src.config import get_settings
from logging import getLogger

logger = getLogger(__name__)

credentials = PlainCredentials(get_settings().rabbitmq_user, get_settings().rabbitmq_password)
parameters = ConnectionParameters(
    host=get_settings().rabbitmq_host,
    port=get_settings().rabbitmq_port,
    credentials=credentials
)
connection = BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

logger.info("Consumer connected to RabbitMQ")

def callback(ch, method, properties, body):
    current_dict = json.loads(body.decode())

    photo_b64 = current_dict["photo"]
    photo_bytes = base64.b64decode(photo_b64)
    result = filter_photo(photo_bytes, current_dict["filter"])

    # Готовим ответ
    result_b64 = base64.b64encode(result).decode('utf-8')
    response = json.dumps({"result": result_b64})

    # Проверяем, есть ли куда отправлять
    if properties.reply_to:
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=response.encode(),
            properties=BasicProperties(correlation_id=properties.correlation_id)
        )
        logger.info("The photo was sent successfully")
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=False)
channel.start_consuming()
