from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.services.storage import upload_file_to_s3
from shared.constants.document_status import DocumentStatus
from app.models import User
from app.db.repositories.document_repo import (
    create_document,
    update_document_status,
)
from shared.messaging.rabbit_mq import publish_message
from shared.messaging.routing_keys import DOCUMENT_PROCESS
from shared.config.logging import get_logger

logger = get_logger(__name__)


async def upload_document(
    file: UploadFile,
    db: Session,
    current_user: User,
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    try:
        logger.info("Uploading file to storage")
        s3_metadata = await upload_file_to_s3(file)

        logger.info("Creating document in database")

        document = create_document(
            db=db,
            user_id=current_user.id,
            original_filename=s3_metadata["original_name"],
            content_type=s3_metadata["content_type"],
            storage_provider="AWS",
            storage_bucket=s3_metadata["bucket"],
            storage_key=s3_metadata["key"],
            status_id=DocumentStatus.QUEUED,
        )

        logger.info("Publishing message to RabbitMQ")
        await publish_message(
            {
                "document_id": str(document.id),
            },
            routing_key=DOCUMENT_PROCESS,
        )

        return {
            "status": "queued",
            "document_id": document.id,
        }

    except Exception:
        logger.exception("Upload failed")

        # Optional but GOOD practice
        if "document" in locals():
            update_document_status(
                db=db,
                document_id=document.id,
                status_id=DocumentStatus.FAILED,
            )

        raise HTTPException(status_code=500, detail="Document upload failed")
