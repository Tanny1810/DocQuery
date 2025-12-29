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
