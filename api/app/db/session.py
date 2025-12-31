from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = (
    f"postgresql://{settings.DB_CONFIG.POSTGRES_USER}:"
    f"{settings.DB_CONFIG.POSTGRES_PASSWORD}@"
    f"{settings.DB_CONFIG.POSTGRES_HOST}:"
    f"{settings.DB_CONFIG.POSTGRES_PORT}/"
    f"{settings.DB_CONFIG.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
