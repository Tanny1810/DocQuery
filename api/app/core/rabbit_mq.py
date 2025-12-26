import json, os
from aio_pika import connect_robust, Message
from api.app.core.config import settings
from shared.config.logging import get_logger

logger = get_logger(__name__)

def get_rabbitmq_url() -> str:
    """Get RabbitMQ URL, using service name in Docker, localhost otherwise"""
    host = settings.QUEUE_CONFIG.RABBITMQ_HOST
    user = settings.QUEUE_CONFIG.RABBITMQ_USER
    password = settings.QUEUE_CONFIG.RABBITMQ_PASSWORD
    port = settings.QUEUE_CONFIG.RABBITMQ_PORT
    
    return f"amqp://{user}:{password}@{host}:{port}/"

RABBITMQ_URL = get_rabbitmq_url()

QUEUE_NAME = settings.QUEUE_CONFIG.QUEUE_NAME


async def publish_message(payload: dict):
    connection = None
    try:
        logger.info("Connecting to RabbitMQ")

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

        logger.info("Message published")

    except Exception:
        logger.exception("Error publishing message to RabbitMQ")
        raise

    finally:
        if connection:
            await connection.close()
            logger.info("Disconnected from RabbitMQ")