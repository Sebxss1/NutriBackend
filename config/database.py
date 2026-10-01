from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config.settings import settings


class Base(DeclarativeBase):
    pass


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    database_url = settings.database_url

    if not database_url:
        raise RuntimeError("DATABASE_URL no está configurada en el archivo .env")

    # Adapta los formatos habituales de URL de Neon al driver psycopg.
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    return create_engine(database_url, pool_pre_ping=True)

def get_db():
    session_factory = sessionmaker(
        bind=get_engine(),
        autoflush=False,
        autocommit=False,
    )
    db: Session = session_factory()

    try:
        yield db
    finally:
        db.close()