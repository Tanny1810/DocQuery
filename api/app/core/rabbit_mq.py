import json
from aio_pika import connect_robust, Message
from api.app.core.config import settings

RABBITMQ_URL = (
    f"amqp://{settings.QUEUE_CONFIG.RABBITMQ_USER}:"
    f"{settings.QUEUE_CONFIG.RABBITMQ_PASSWORD}@"
    f"{settings.QUEUE_CONFIG.RABBITMQ_HOST}:"
    f"{settings.QUEUE_CONFIG.RABBITMQ_PORT}/"
)

QUEUE_NAME = settings.QUEUE_CONFIG.QUEUE_NAME


async def publish_message(payload: dict):
    connection = None
    try:
        print("Connecting to RabbitMQ")

        connection = await connect_robust(RABBITMQ_URL)
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        message = Message(
            body=json.dumps(payload).encode(),
            delivery_mode=2,
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )

        print("Message published")

    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {e}")
        raise

    finally:
        if connection:
            await connection.close()
            print("Disconnected from RabbitMQ")