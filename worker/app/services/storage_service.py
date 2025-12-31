from pathlib import Path
import tempfile

from app.services.storage_providers.aws import download_from_s3

# later:
# from app.services.storage_providers.gcs import download_from_gcs
# from app.services.storage_providers.azure import download_from_azure


def download_file(*, provider: str, bucket: str, key: str) -> Path:
    """
    Download a file from object storage and return local file path.
    """

    tmp_dir = Path(tempfile.mkdtemp(prefix="docquery_"))
    local_path = tmp_dir / Path(key).name

    if provider == "AWS":
        download_from_s3(
            bucket=bucket,
            key=key,
            destination=local_path,
        )
    else:
        raise ValueError(f"Unsupported storage provider: {provider}")

    return local_path
