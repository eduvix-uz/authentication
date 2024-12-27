import asyncio
import aio_pika
from django.conf import settings


async def main():
    connection = await aio_pika.connect_robust(f'{settings.RABBITMQ_URL}')
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body="Hello, RabbitMQ!".encode()),
            routing_key="test_queue"
        )
    print("Message sent!")

