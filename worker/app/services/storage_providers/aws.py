import boto3
from pathlib import Path
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.CLOUD_CONFIG.AWS_TE_ACCESS_KEY_ID,
    aws_secret_access_key=settings.CLOUD_CONFIG.AWS_TE_SECRET_ACCESS_KEY,
    region_name=settings.CLOUD_CONFIG.AWS_REGION,
)


def download_from_s3(*, bucket: str, key: str, destination: Path) -> None:
    """
    Download file from AWS S3 to local destination.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)

    s3_client.download_file(
        Bucket=bucket,
        Key=key,
        Filename=str(destination),
    )