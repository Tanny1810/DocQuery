import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings

def get_connection():
    return psycopg2.connect(
        host=settings.DB_CONFIG.POSTGRES_HOST,
        port=settings.DB_CONFIG.POSTGRES_PORT,
        user=settings.DB_CONFIG.POSTGRES_USER,
        password=settings.DB_CONFIG.POSTGRES_PASSWORD,
        dbname=settings.DB_CONFIG.POSTGRES_DB,
        cursor_factory=RealDictCursor,
    )
