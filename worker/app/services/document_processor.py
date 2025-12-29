from app.services.storage_service import download_file
from app.processors.text_extractor import extract_text
from app.processors.chunker import chunk_text
from app.processors.embedder import embed_chunks
from app.db.vector_store import store_embeddings, get_vector_count
from app.db.document_repo import (
    update_document_status,
    get_document_storage_info,
)
from app.constants.document_status import DocumentStatus
from shared.config.logging import get_logger

logger = get_logger(__name__)


async def process_document(payload: dict):
    document_id = payload["document_id"]

    logger.info(f"📄 Processing document {document_id}")

    update_document_status(document_id, DocumentStatus.PROCESSING)

    file_path = None

    try:
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

        # 4️⃣ Chunk text
        chunks = chunk_text(text)

        if not chunks:
            raise ValueError("No chunks generated from document")

        # 5️⃣ Embed
        embeddings = embed_chunks(chunks)

        # 6️⃣ Store embeddings
        store_embeddings(embeddings)

        logger.info(f"✅ Stored {len(embeddings)} embeddings")
        logger.info(f"📊 Total vectors in FAISS: {get_vector_count()}")

        # 7️⃣ Mark READY
        update_document_status(document_id, DocumentStatus.READY)

    except Exception as exc:
        logger.exception(
            f"❌ Failed processing document {document_id}: {exc}"
        )
        update_document_status(document_id, DocumentStatus.RETRYING)
        raise

    finally:
        # 8️⃣ Cleanup temp file
        if file_path:
            try:
                file_path.unlink(missing_ok=True)
            except Exception:
                logger.warning(
                    f"⚠️ Failed to cleanup temp file {file_path}"
                )
