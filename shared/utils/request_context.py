from contextvars import ContextVar
from typing import Optional

_REQUEST_ID: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def set_request_id(rid: str) -> None:
    _REQUEST_ID.set(rid)


def get_request_id() -> Optional[str]:
    return _REQUEST_ID.get()
