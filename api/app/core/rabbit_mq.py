import json
from aio_pika import connect_robust, Message
from api.app.core.config import settings


RABBITMQ_URL = f"amqp://{settings.QUEUE_CONFIG.RABBITMQ_USER}:{settings.QUEUE_CONFIG.RABBITMQ_PASSWORD}@{settings.QUEUE_CONFIG.RABBITMQ_HOST}:{settings.QUEUE_CONFIG.RABBITMQ_PORT}/"
QUEUE_NAME = settings.QUEUE_CONFIG.QUEUE_NAME


async def publish_message(payload: dict):
    connection = await connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        message = Message(
            body=json.dumps(payload).encode(),
            delivery_mode=2
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )
