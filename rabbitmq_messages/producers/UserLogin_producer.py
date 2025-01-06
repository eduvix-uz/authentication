import aio_pika
import json
from django.conf import settings

async def user_login(username, user_id, is_staff, email, first_name, last_name):
    connection = await aio_pika.connect_robust(f'{settings.RABBITMQ_URL}')
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue("user_login_queue", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"username": username, "user_id": user_id, "is_admin": is_staff, "email": email, "first_name": first_name, "last_name": last_name}).encode()),
            routing_key="user_login_queue",
        )