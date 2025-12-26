import boto3
from pathlib import Path
from app.config import settings


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.CLOUD_CONFIG.AWS_TE_ACCESS_KEY_ID,
    aws_secret_access_key=settings.CLOUD_CONFIG.AWS_TE_SECRET_ACCESS_KEY,
    region_name=settings.CLOUD_CONFIG.AWS_REGION,
)


def download_file_from_s3(bucket: str, key: str) -> Path:
    local_path = Path("/tmp") / key.replace("/", "_")
    local_path.parent.mkdir(parents=True, exist_ok=True)

    s3_client.download_file(bucket, key, str(local_path))
    return local_path
