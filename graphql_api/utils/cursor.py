import base64
from datetime import datetime


def encode_cursor(created_at: datetime, doc_id: str) -> str:
    raw = f"{created_at.isoformat()}|{doc_id}"
    return base64.b64encode(raw.encode()).decode()


def decode_cursor(cursor: str) -> tuple[datetime, str]:
    raw = base64.b64decode(cursor).decode()
    created_at_str, doc_id = raw.split("|")
    return datetime.fromisoformat(created_at_str), doc_id
