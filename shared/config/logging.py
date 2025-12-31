import logging
import sys
from typing import Optional

try:
    from shared.utils.request_context import get_request_id
except Exception:

    def get_request_id():
        return None


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        try:
            record.request_id = get_request_id() or "-"
        except Exception:
            record.request_id = "-"
        return True


def configure_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    fmt = "%(asctime)s %(levelname)s [%(request_id)s] %(name)s: %(message)s"
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    root.handlers = []
    handler.addFilter(RequestIDFilter())
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
