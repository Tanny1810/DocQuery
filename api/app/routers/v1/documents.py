from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from api.app.services.storage import upload_file_to_s3
from api.app.core.rabbit_mq import publish_message
from api.app.constants.document_status import DocumentStatus
from api.app.db.repositories.document_repo import create_document, update_document_status
from api.app.db.session import get_db
from shared.config.logging import get_logger


logger = get_logger(__name__)

router = APIRouter()


@router.post(path="/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        logger.error("Invalid file")
        raise HTTPException(status_code=400, detail="Invalid file")

    logger.info("Uploading file to S3")

    s3_metadata = await upload_file_to_s3(file)

    logger.info("Successfully uploaded file to S3")
    logger.debug("S3 Metadata: %s", s3_metadata)
    logger.info("Creating document in database")

    document = create_document(
        db=db,
        original_filename=s3_metadata.get("original_name"),
        content_type=s3_metadata.get("content_type"),
        storage_provider="AWS",
        storage_bucket=s3_metadata.get("bucket"),
        storage_key=s3_metadata.get("key"),
    )

    logger.info("Publishing message to RabbitMQ")

    publish_message({
        "document_id": str(document.id),
    })

    logger.info("Message published to RabbitMQ")
    logger.info("Updating document status to QUEUED")

    update_document_status(
        db=db,
        document_id=document.id,
        status_id=DocumentStatus.QUEUED,
    )

    return {
        "status": "uploaded",
        "s3_bucket": s3_metadata["bucket"],
        "s3_key": s3_metadata["key"],
    }
