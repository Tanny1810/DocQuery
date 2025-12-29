from uuid import UUID
from app.services.storage_service import download_file_from_s3
from app.processors.text_extractor import extract_text
from app.processors.chunker import chunk_text
from app.processors.embedder import embed_chunks
from app.db.vector_store import store_embeddings, get_vector_count
from app.db.document_repo import update_document_status
from app.constants.document_status import DocumentStatus
from shared.config.logging import get_logger

logger = get_logger(__name__)

async def process_document(payload: dict):
    # Explicit + defensive
    document_id = UUID(payload["document_id"])

    update_document_status(document_id, DocumentStatus.PROCESSING)

    try:
        # download → extract → chunk → embed → store

        file_path = download_file_from_s3(bucket, key)

        text = extract_text(file_path)
        chunks = chunk_text(text)

        embeddings = embed_chunks(chunks)
        store_embeddings(embeddings)

        logger.info(f"✅ Stored {len(embeddings)} embeddings")
        logger.info(f"📊 Total vectors in FAISS: {get_vector_count()}")
        
        update_document_status(document_id, DocumentStatus.READY)

    except Exception:
        update_document_status(document_id, DocumentStatus.RETRYING)
        raise