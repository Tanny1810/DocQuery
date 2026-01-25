from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.repositories.query_audit_repo import count_queries_since
from app.core.config import settings


# V2: simple daily quota
DAILY_QUERY_LIMIT = 5


class RateLimitExceeded(Exception):
    pass


def check_rate_limit(
    *,
    db: Session,
    user_id,
):
    since = datetime.now() - timedelta(days=1)

    query_count = count_queries_since(db, user_id, since)

    if query_count >= settings.DAILY_QUERY_LIMIT:
        raise RateLimitExceeded(
            f"Daily query limit of {DAILY_QUERY_LIMIT} exceeded"
        )
