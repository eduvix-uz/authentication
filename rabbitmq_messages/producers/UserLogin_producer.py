import json
import aio_pika
from django.conf import settings
import os

async def user_login(username, user_id, is_staff, email, first_name, last_name):
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
    try:
        # Establish a connection to RabbitMQ
        connection = await aio_pika.connect_robust(rabbitmq_url, timeout=3)
        async with connection:
            # Create a channel
            channel = await connection.channel()
            
            # Declare a durable queue (ensure it persists even if RabbitMQ restarts)
            queue = await channel.declare_queue("user_login_queue", durable=True)
            
            # Prepare the message
            message_body = json.dumps({
                "username": username,
                "user_id": user_id,
                "is_admin": is_staff,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            })
            message = aio_pika.Message(body=message_body.encode())

            # Publish the message to the queue
            await channel.default_exchange.publish(
                message,
                routing_key=queue.name,
            )
            # print(f"Message published to {queue.name}: {message_body}")
            channel.close()
    except aio_pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
