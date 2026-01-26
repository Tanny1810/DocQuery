import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from app.services.document_processor import process_document
from shared.messaging.rabbit_mq import get_rabbitmq_url
from app.messaging.bootstrap import setup_rabbitmq
from shared.config.logging import get_logger

logger = get_logger(__name__)


async def handle_message(message: IncomingMessage):
    async with message.process():
        body = json.loads(message.body)
        payload = body.get("payload")
        if not payload:
            raise ValueError("Invalid message format: missing payload")
        meta = body.get("meta", {})
        logger.info("📩 Received document job")
        await process_document(payload)


async def start_document_consumer():
    RABBITMQ_URL = get_rabbitmq_url()

    logger.info("🔌 Connecting to RabbitMQ...")
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    queue_main, queue_retry = await setup_rabbitmq(channel)

    await queue_main.consume(handle_message)
    await queue_retry.consume(handle_message)

    logger.info("👂 Worker listening for document ingestion jobs...")

    # 🔥 KEEP PROCESS ALIVE
    await asyncio.Future()  # runs forever
