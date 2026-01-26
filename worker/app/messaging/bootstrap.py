from aio_pika import ExchangeType
from app.core.config import settings


async def setup_rabbitmq(channel):
    exchange = await channel.declare_exchange(
        settings.QUEUE_CONFIG.RABBITMQ_EXCHANGE,
        ExchangeType.TOPIC,
        durable=True,
    )

    queue_main = await channel.declare_queue(
        settings.QUEUE_CONFIG.QUEUE_MAIN,
        durable=True,
    )

    queue_retry = await channel.declare_queue(
        settings.QUEUE_CONFIG.QUEUE_RETRY,
        durable=True,
    )

    queue_dlq = await channel.declare_queue(
        settings.QUEUE_CONFIG.QUEUE_DLQ,
        durable=True,
    )

    # 🔑 Routing key bindings
    await queue_main.bind(exchange, routing_key="document.process")
    await queue_retry.bind(exchange, routing_key="document.retry")
    await queue_dlq.bind(exchange, routing_key="document.dlq")

    return queue_main, queue_retry
