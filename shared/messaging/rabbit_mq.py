import json
from urllib.parse import quote_plus
from aio_pika import connect_robust, Message, ExchangeType, DeliveryMode
from app.core.config import settings
from shared.config.logging import get_logger

logger = get_logger(__name__)


def get_rabbitmq_url() -> str:
    host = settings.QUEUE_CONFIG.RABBITMQ_HOST
    user = quote_plus(settings.QUEUE_CONFIG.RABBITMQ_USER)
    password = quote_plus(settings.QUEUE_CONFIG.RABBITMQ_PASSWORD)
    port = settings.QUEUE_CONFIG.RABBITMQ_PORT
    return f"amqp://{user}:{password}@{host}:{port}/"


RABBITMQ_URL = get_rabbitmq_url()
EXCHANGE_NAME = settings.QUEUE_CONFIG.RABBITMQ_EXCHANGE


async def publish_message(payload: dict, routing_key: str):
    """
    Publish an event to RabbitMQ using topic-based routing.

    Producers do NOT know queues.
    They publish semantic events via routing keys.
    """
    connection = None
    try:
        logger.info(
            "📨 Publishing message",
            extra={
                "exchange": EXCHANGE_NAME,
                "routing_key": routing_key,
            },
        )

        connection = await connect_robust(RABBITMQ_URL)
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            EXCHANGE_NAME,
            ExchangeType.TOPIC,
            durable=True,
        )

        message_body = {
            "payload": payload,
            "meta": {
                "routing_key": routing_key,
            },
        }

        message = Message(
            body=json.dumps(message_body).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await exchange.publish(
            message,
            routing_key=routing_key,
        )

        logger.info("✅ Message published")

    except Exception:
        logger.exception("❌ Error publishing message to RabbitMQ")
        raise

    finally:
        if connection:
            await connection.close()
            logger.info("🔌 Disconnected from RabbitMQ")
