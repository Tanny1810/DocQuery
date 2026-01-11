from app.services.storage_service import download_file
from app.processors.text_extractor import extract_text, clean_text
from app.processors.chunker import chunk_text
from shared.embeddings.embedder import embed_chunks
from app.db.vector_store import store_embeddings, get_vector_count
from app.db.document_repo import (
    update_document_status,
    get_document_storage_info,
    get_document_for_update,
    insert_chunks,
)
from app.services.document_retry_service import increment_retry_or_fail
from shared.constants.document_status import DocumentStatus
from shared.config.logging import get_logger

logger = get_logger(__name__)


async def process_document(payload: dict):
    document_id = payload["document_id"]

    logger.info(f"📄 Processing document {document_id}")

    doc = get_document_for_update(document_id)

    if doc["status_id"] != DocumentStatus.QUEUED:
        logger.info(f"⏭️ Skipping document {document_id}, " f"status={doc['status_id']}")
        return

    file_path = None

    try:
        # 0️⃣ Mark PROCESSING
        update_document_status(document_id, DocumentStatus.PROCESSING)
        # 1️⃣ Fetch storage info from DB (SOURCE OF TRUTH)
        storage = get_document_storage_info(document_id)

        # 2️⃣ Download file
        file_path = download_file(
            provider=storage["storage_provider"],
            bucket=storage["storage_bucket"],
            key=storage["storage_key"],
        )

        # 3️⃣ Extract text
        text = extract_text(file_path)

        # 🔧 CLEAN HERE
        text = clean_text(text)

        # 4️⃣ Chunk text
        chunks = chunk_text(text)

        if not chunks:
            raise ValueError("No chunks generated from document")

        # 5️⃣ Embed
        embeddings = embed_chunks(chunks)

        # 6️⃣ Store embeddings
        vector_ids = store_embeddings(embeddings)

        logger.info(f"✅ Stored {len(embeddings)} embeddings")
        logger.info(f"📊 Total vectors in FAISS: {get_vector_count()}")

        insert_chunks(
            document_id=document_id,
            chunks=chunks,
            vector_ids=vector_ids,
        )
        logger.info(f"✅ Stored {len(chunks)} chunks")

        # 7️⃣ Mark READY
        update_document_status(document_id, DocumentStatus.READY)

    except Exception as exc:
        logger.exception(f"❌ Failed processing document {document_id}: {exc}")
        increment_retry_or_fail(document_id, exc)
        return

    finally:
        # 8️⃣ Cleanup temp file
        if file_path:
            try:
                logger.info(f"🧹 Cleaning up temp file {file_path}")
                file_path.unlink(missing_ok=True)
            except Exception:
                logger.warning(f"⚠️ Failed to cleanup temp file {file_path}")
