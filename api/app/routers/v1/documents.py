from fastapi import APIRouter, UploadFile, File, HTTPException
from api.app.services.storage import upload_file_to_s3
from api.app.core.rabbit_mq import publish_message

router = APIRouter()


@router.post(path="/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")
    print("Uploading file to S3")
    s3_metadata = await upload_file_to_s3(file)
    print("Successfully uploaded file to S3")
    print("S3 Metadata:", s3_metadata)

    print("Publishing message to RabbitMQ")
    await publish_message(s3_metadata)
    print("Message published to RabbitMQ")

    return {
        "status": "uploaded",
        "s3_bucket": s3_metadata["bucket"],
        "s3_key": s3_metadata["key"],
    }
