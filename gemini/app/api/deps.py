"""Contém as dependências da API."""

from typing import Generator

from app.core.database import SessionLocal


def get_db() -> Generator:
    """
    Obtém uma sessão do banco de dados.

    Yields:
        Uma sessão do banco de dados.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
