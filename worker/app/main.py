# Worker main application

import asyncio
from shared.config.logging import configure_logging
from app.consumers.document_consumer import start_document_consumer
from app.core.config import settings


if __name__ == "__main__":
    # configure global logging early
    configure_logging(settings.LOG_LEVEL)
    asyncio.run(
        start_document_consumer(
            queue_name=settings.QUEUE_CONFIG.QUEUE_NAME,
        )
    )
