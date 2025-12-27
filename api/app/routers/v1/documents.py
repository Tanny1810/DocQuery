from math import log
from fastapi import APIRouter, UploadFile, File, HTTPException
from api.app.services.storage import upload_file_to_s3
from api.app.core.rabbit_mq import publish_message
from shared.config.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(path="/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")
    logger.info("Uploading file to S3")
    s3_metadata = await upload_file_to_s3(file)
    logger.info("Successfully uploaded file to S3")
    logger.debug("S3 Metadata: %s", s3_metadata)

    logger.info("Publishing message to RabbitMQ")
    await publish_message(s3_metadata)
    logger.info("Message published to RabbitMQ")

    return {
        "status": "uploaded",
        "s3_bucket": s3_metadata["bucket"],
        "s3_key": s3_metadata["key"],
    }
