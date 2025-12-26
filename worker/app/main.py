# Worker main application

import asyncio
from app.consumers.document_consumer import start_document_consumer
from app.config import settings


if __name__ == "__main__":
    asyncio.run(
        start_document_consumer(
            queue_name=settings.QUEUE_CONFIG.QUEUE_NAME,
        )
    )
