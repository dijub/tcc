from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# Cria o Engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,      # valida conexões já abertas
    echo=settings.ECHO_SQL,  # mostra SQL no stdout, se ativado
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para injeção de sessão no FastAPI (sem rotas ainda).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 