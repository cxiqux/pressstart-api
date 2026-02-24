import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings


def get_connection():
    return psycopg2.connect(settings.DATABASE_URL, cursor_factory=RealDictCursor)


def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()