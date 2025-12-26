import asyncio
import json
import aio_pika
from app.services.document_processor import process_document
from app.config import settings


def get_rabbitmq_url() -> str:
    host = settings.QUEUE_CONFIG.RABBITMQ_HOST
    user = settings.QUEUE_CONFIG.RABBITMQ_USER
    password = settings.QUEUE_CONFIG.RABBITMQ_PASSWORD
    port = settings.QUEUE_CONFIG.RABBITMQ_PORT

    return f"amqp://{user}:{password}@{host}:{port}/"


async def handle_message(message: aio_pika.IncomingMessage):
    async with message.process():
        payload = json.loads(message.body)
        print("📩 Received document job")
        await process_document(payload)


async def start_document_consumer(queue_name: str):
    rabbitmq_url = get_rabbitmq_url()

    print("🔌 Connecting to RabbitMQ...")
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(queue_name, durable=True)

    await queue.consume(handle_message)

    print("👂 Worker listening for document ingestion jobs...")

    # 🔥 KEEP PROCESS ALIVE
    await asyncio.Future()  # runs forever
