from app.core.config import settings
from app.db.document_repo import (
    get_document_for_update,
    increment_retry_count,
    update_document_status,
)
from shared.constants.document_status import DocumentStatus
from shared.messaging.rabbit_mq import publish_message
from shared.messaging.routing_keys import DOCUMENT_RETRY, DOCUMENT_DLQ
from shared.config.logging import get_logger

logger = get_logger(__name__)


async def increment_retry_or_fail(document_id, exc: Exception):
    doc = get_document_for_update(document_id)

    if doc["retry_count"] < doc["max_retries"]:
        increment_retry_count(document_id)

        update_document_status(
            document_id,
            DocumentStatus.RETRYING,
        )

        await publish_message(
            {
                "document_id": str(document_id),
                "retry": True,
                "attempt": doc["retry_count"] + 1,
            },
            routing_key=DOCUMENT_RETRY,
        )

        logger.warning(
            f"🔁 Retrying document {document_id} "
            f"({doc['retry_count'] + 1}/{doc['max_retries']})"
        )

    else:
        update_document_status(
            document_id,
            DocumentStatus.FAILED,
        )

        await publish_message(
            {
                "document_id": str(document_id),
                "reason": "MAX_RETRIES_EXCEEDED",
                "retry_count": doc["retry_count"],
                "error": str(exc),
            },
            routing_key=DOCUMENT_DLQ,
        )

        logger.error(f"☠️ Document {document_id} sent to DLQ")
