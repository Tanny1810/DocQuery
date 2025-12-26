from uuid import uuid4
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from shared.utils.request_context import set_request_id, get_request_id
from shared.config.logging import get_logger

logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-Id") or uuid4().hex
        set_request_id(rid)
        start = time.time()

        response = await call_next(request)

        duration_ms = (time.time() - start) * 1000
        # ensure header present
        response.headers.setdefault("X-Request-Id", rid)

        try:
            logger.info(
                f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.2f}ms)"
            )
        except Exception:
            pass

        return response
