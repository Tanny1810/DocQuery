from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from api.app.services.storage import upload_file_to_s3
from api.app.constants.document_status import DocumentStatus
from api.app.db.repositories.document_repo import (
    create_document,
    update_document_status,
)
from api.app.db.session import get_db
from shared.messaging.rabbit_mq import publish_message
from shared.config.logging import get_logger


logger = get_logger(__name__)

router = APIRouter()


@router.post(path="/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    try:
        logger.info("Uploading file to storage")
        s3_metadata = await upload_file_to_s3(file)

        logger.info("Creating document in database")

        document = create_document(
            db=db,
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
            }
        )

        return {
            "status": "queued",
            "document_id": document.id,
        }

    except Exception as e:
        logger.exception("Upload failed")

        # Optional but GOOD practice
        if "document" in locals():
            update_document_status(
                db=db,
                document_id=document.id,
                status_id=DocumentStatus.FAILED,
            )

        raise HTTPException(status_code=500, detail="Document upload failed")
