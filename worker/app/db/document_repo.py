from app.db.postgres import get_connection
from app.constants.document_status import DocumentStatus
from psycopg2.extras import execute_values

MAX_RETRIES = 3


def update_document_status(document_id, status_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE documents
        SET status_id = %s
        WHERE id = %s
        """,
        (status_id, document_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_document_storage_info(document_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            storage_provider,
            storage_bucket,
            storage_key
        FROM documents
        WHERE id = %s
        """,
        (str(document_id),),
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        raise ValueError(f"Document {document_id} not found")

    return {
        "storage_provider": row["storage_provider"],
        "storage_bucket": row["storage_bucket"],
        "storage_key": row["storage_key"],
    }


def get_document_for_update(document_id):
    """
    Fetch document row with FOR UPDATE lock.
    Ensures only one worker processes a document at a time.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            status_id,
            storage_provider,
            storage_bucket,
            storage_key,
            retry_count,
            max_retries
        FROM documents
        WHERE id = %s
        FOR UPDATE
        """,
        (str(document_id),),
    )

    row = cur.fetchone()

    if row is None:
        cur.close()
        conn.close()
        raise ValueError(f"Document {document_id} not found")

    # IMPORTANT:
    # Do NOT close connection here — caller logic continues in same txn
    # Status updates happen in separate statements

    cur.close()
    conn.commit()
    conn.close()

    return row


def insert_chunks(document_id, chunks, vector_ids):
    conn = get_connection()
    cur = conn.cursor()

    values = [
        (document_id, idx, content, vector_id)
        for idx, (content, vector_id) in enumerate(zip(chunks, vector_ids))
    ]

    query = """
        INSERT INTO chunks (document_id, chunk_index, content, vector_id)
        VALUES %s
        ON CONFLICT (document_id, chunk_index) DO NOTHING
    """

    execute_values(cur, query, values)

    conn.commit()
    cur.close()
    conn.close()


def increment_retry_count(document_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE documents
        SET retry_count = retry_count + 1
        WHERE id = %s
        """,
        (str(document_id),),
    )

    conn.commit()
    cur.close()
    conn.close()


def get_chunks_for_rag(vector_ids: list[int]):
    """
    Validate FAISS results against Postgres.
    Only READY / PARTIAL documents are allowed.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.document_id,
            c.chunk_index,
            c.content,
            c.vector_id,
            d.status_id
        FROM chunks c
        JOIN documents d ON d.id = c.document_id
        WHERE c.vector_id = ANY(%s)
          AND d.status_id IN (%s, %s)
        """,
        (
            vector_ids,
            DocumentStatus.READY,
            DocumentStatus.PARTIAL,
        ),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows
