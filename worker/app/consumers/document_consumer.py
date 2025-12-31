import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from app.services.document_processor import process_document
from shared.messaging.rabbit_mq import get_rabbitmq_url
from shared.config.logging import get_logger

logger = get_logger(__name__)


async def handle_message(message: IncomingMessage):
    async with message.process():
        payload = json.loads(message.body)
        logger.info("📩 Received document job")
        await process_document(payload)


async def start_document_consumer(queue_name: str):
    RABBITMQ_URL = get_rabbitmq_url()

    logger.info("🔌 Connecting to RabbitMQ...")
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(queue_name, durable=True)

    await queue.consume(handle_message)

    logger.info("👂 Worker listening for document ingestion jobs...")

    # 🔥 KEEP PROCESS ALIVE
    await asyncio.Future()  # runs forever
