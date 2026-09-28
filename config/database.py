from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config.settings import settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    database_url = settings.database_url
    if not database_url:
        raise RuntimeError("DATABASE_URL no esta configurada")

    # Acepta formatos habituales de URL PostgreSQL de Neon y Render.
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://", "postgresql+psycopg://", 1
        )
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )

    return create_engine(database_url, pool_pre_ping=True)
