from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from typing import Generator

# Configuração da URL do banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/database_name"
)

# Configuração do engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    # Configurações de pool de conexões
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verifica se a conexão está ativa antes de usar
    pool_recycle=300,    # Recicla conexões a cada 5 minutos
    echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"  # Log SQL queries
)

# Configuração da sessão
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para os modelos
Base = declarative_base()

def get_db() -> Generator:
    """
    Função para obter uma sessão do banco de dados.
    Utilizada como dependência no FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Cria todas as tabelas definidas nos modelos.
    Deve ser chamada no início da aplicação.
    """
    Base.metadata.create_all(bind=engine)

def check_database_connection() -> bool:
    """
    Verifica se a conexão com o banco de dados está funcionando.
    Retorna True se conectado, False caso contrário.
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return False 