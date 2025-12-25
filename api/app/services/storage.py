import boto3
from fastapi import UploadFile
from api.app.core.config import settings
from api.app.core.utils import generate_uuid


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.CLOUD_CONFIG.AWS_TE_ACCESS_KEY_ID,
    aws_secret_access_key=settings.CLOUD_CONFIG.AWS_TE_SECRET_ACCESS_KEY,
    region_name=settings.CLOUD_CONFIG.AWS_REGION,
)

BUCKET_NAME = settings.CLOUD_CONFIG.S3_BUCKET_NAME


async def upload_file_to_s3(file: UploadFile) -> dict:
    file_id = generate_uuid()
    s3_key = f"documents/{file_id}_{file.filename}"

    s3_client.upload_fileobj(
        file.file,
        BUCKET_NAME,
        s3_key,
        ExtraArgs={"ContentType": file.content_type},
    )

    return {
        "bucket": BUCKET_NAME,
        "key": s3_key,
        "original_name": file.filename,
        "content_type": file.content_type,
    }
