from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import get_engine

app = FastAPI(
    title="Nutri API",
    description="API REST para el proyecto Nutri.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"mensaje": "API de Nutri en funcionamiento"}


@app.get("/health", tags=["Salud"])
def health():
    """Comprobacion de disponibilidad usada por Render."""
    return {"estado": "ok"}


@app.get("/health/db", tags=["Salud"])
def health_database():
    """Comprueba que la API puede ejecutar una consulta en PostgreSQL."""
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(
            status_code=503,
            detail="Base de datos no disponible; revisa DATABASE_URL en la configuracion.",
        ) from error

    return {"estado": "ok", "base_de_datos": "conectada"}
