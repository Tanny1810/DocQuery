from app.services.storage_service import download_file
from app.services.document_retry_service import increment_retry_or_fail
from app.processors.chunker import chunk_pages
from app.processors.extractor_factory import get_extractor
from app.db.vector_store import store_embeddings, get_vector_count
from app.db.document_repo import (
    update_document_status,
    get_document_storage_info,
    get_document_for_update,
    insert_chunks,
)
from shared.embeddings.embedder import embed_chunks
from shared.constants.document_status import DocumentStatus
from shared.config.logging import get_logger

logger = get_logger(__name__)


async def process_document(payload: dict):
    document_id = payload["document_id"]

    logger.info(f"📄 Processing document {document_id}")

    doc = get_document_for_update(document_id)

    if doc["status_id"] not in (
        DocumentStatus.QUEUED,
        DocumentStatus.RETRYING,
    ):
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
        # 3️⃣ Get extractor via factory (format-agnostic)
        extractor = get_extractor(file_path)
        blocks = extractor.extract(file_path)

        if not blocks:
            raise ValueError("No text extracted from document")
        
        for i, block in enumerate(blocks):
            if "text" not in block:
                raise ValueError(
                    f"Invalid block at index {i}: missing 'text' key. Block={block}"
                )

        # 4️⃣ Page-aware chunking
        chunks = chunk_pages(blocks)

        if not chunks:
            raise ValueError("No chunks generated from document")

        # 5️⃣ Embed ONLY chunk content
        texts = [c["content"] for c in chunks]
        embeddings = embed_chunks(texts)

        # 6️⃣ Store embeddings
        vector_ids = store_embeddings(embeddings)

        logger.info(f"✅ Stored {len(embeddings)} embeddings")
        logger.info(f"📊 Total vectors in FAISS: {get_vector_count()}")

        # 7️⃣ Persist chunks with page_number
        insert_chunks(
            document_id=document_id,
            chunks=chunks,
            vector_ids=vector_ids,
        )

        logger.info(f"✅ Stored {len(chunks)} chunks")

        # 8️⃣ Mark READY
        update_document_status(document_id, DocumentStatus.READY)

    except Exception as exc:
        logger.exception(f"❌ Failed processing document {document_id}: {exc}")
        await increment_retry_or_fail(document_id, exc)
        return

    finally:
        # 8️⃣ Cleanup temp file
        if file_path:
            try:
                logger.info(f"🧹 Cleaning up temp file {file_path}")
                file_path.unlink(missing_ok=True)
            except Exception:
                logger.warning(f"⚠️ Failed to cleanup temp file {file_path}")
