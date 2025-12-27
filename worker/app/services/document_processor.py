from app.services.storage_service import download_file_from_s3
from app.processors.text_extractor import extract_text
from app.processors.chunker import chunk_text
from app.processors.embedder import embed_chunks
from app.db.vector_store import store_embeddings, get_vector_count
from shared.config.logging import get_logger

logger = get_logger(__name__)

async def process_document(payload: dict):
    bucket = payload["bucket"]
    key = payload["key"]

    file_path = download_file_from_s3(bucket, key)

    text = extract_text(file_path)
    chunks = chunk_text(text)

    embeddings = embed_chunks(chunks)
    store_embeddings(embeddings)

    logger.info(f"✅ Stored {len(embeddings)} embeddings")
    logger.info(f"📊 Total vectors in FAISS: {get_vector_count()}")