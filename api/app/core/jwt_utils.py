from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import User


def get_user_from_token(token: str, db: Session) -> User | None:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = payload.get("sub")
        if not user_id:
            return None
    except JWTError:
        return None

    return db.query(User).filter(User.id == user_id).first()
