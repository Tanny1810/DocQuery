import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from app.services.document_processor import process_document
from app.config import settings


def get_rabbitmq_url() -> str:
    host = settings.QUEUE_CONFIG.RABBITMQ_HOST
    user = settings.QUEUE_CONFIG.RABBITMQ_USER
    password = settings.QUEUE_CONFIG.RABBITMQ_PASSWORD
    port = settings.QUEUE_CONFIG.RABBITMQ_PORT

    return f"amqp://{user}:{password}@{host}:{port}/"


async def handle_message(message: IncomingMessage):
    async with message.process():
        payload = json.loads(message.body)
        print("📩 Received document job")
        await process_document(payload)


async def start_document_consumer(queue_name: str):
    RABBITMQ_URL = get_rabbitmq_url()

    print("🔌 Connecting to RabbitMQ...")
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(queue_name, durable=True)

    await queue.consume(handle_message)

    print("👂 Worker listening for document ingestion jobs...")

    # 🔥 KEEP PROCESS ALIVE
    await asyncio.Future()  # runs forever
