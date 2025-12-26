from app.services.storage_service import download_file_from_s3


async def process_document(payload: dict):
    bucket = payload["bucket"]
    key = payload["key"]

    print(f"⚙️ Processing document s3://{bucket}/{key}")

    local_path = download_file_from_s3(bucket, key)

    print(f"📂 File downloaded to {local_path}")

    # NEXT STEPS (later):
    # text = extract_text(local_path)
    # chunks = chunk_text(text)
    # embeddings = embed(chunks)
    # store_embeddings(embeddings)
