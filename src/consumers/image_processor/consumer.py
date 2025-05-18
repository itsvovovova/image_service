import base64
import json
from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.spec import BasicProperties
from filter_photo import filter_photo

connection = BlockingConnection(
    ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    current_dict = json.loads(body.decode())  # декодируем bytes -> str -> dict

    print(f"Received {current_dict}")

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
        print(f" [x] Sent result to {properties.reply_to}")
    else:
        print(" [!] No reply_to specified, result not sent.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("Done")
channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()