from app.constants.document_status import DocumentStatus
from app.db.document_repo import (
    get_document_for_update,
    increment_retry_count,
    update_document_status,
)
from shared.messaging.rabbit_mq import publish_message
from shared.config.logging import get_logger

logger = get_logger(__name__)

MAIN_QUEUE = "document_ingestion"
DLQ_QUEUE = "document_ingestion.dlq"


def increment_retry_or_fail(document_id, exc: Exception):
    doc = get_document_for_update(document_id)

    if doc["retry_count"] < doc["max_retries"]:
        increment_retry_count(document_id)

        update_document_status(
            document_id,
            DocumentStatus.RETRYING,
        )

        publish_message(
            {"document_id": str(document_id)},
            queue=MAIN_QUEUE,
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

        publish_message(
            {
                "document_id": str(document_id),
                "reason": "MAX_RETRIES_EXCEEDED",
                "retry_count": doc["retry_count"],
                "error": str(exc),
            },
            queue=DLQ_QUEUE,
        )

        logger.error(
            f"☠️ Document {document_id} sent to DLQ"
        )
