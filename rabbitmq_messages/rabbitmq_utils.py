import pika
import json
from decouple import config

RABBITMQ_HOST = config('RABBITMQ_HOST')
RABBITMQ_PORT = config('RABBITMQ_PORT')
RABBITMQ_USER = config('RABBITMQ_USER')
RABBITMQ_PASSWORD = config('RABBITMQ_PASSWORD')

def publish_message(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        RABBITMQ_HOST, 
        RABBITMQ_PORT, 
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)))
    
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Declare exchange
    channel.exchange_declare(exchange='auth_service', exchange_type='direct', durable=True)

    # Bind queue to exchange
    channel.queue_bind(exchange='auth_service', queue=queue_name, routing_key=queue_name)

    # Set message properties
    properties = pika.BasicProperties(
        delivery_mode=2,
    )

    # Publish the message
    channel.basic_publish(
        exchange='auth_service',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2, 
        )
    )

    channel.close()
    connection.close()