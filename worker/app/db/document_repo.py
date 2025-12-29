from app.db.postgres import get_connection

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