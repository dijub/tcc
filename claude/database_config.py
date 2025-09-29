from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
import logging
from config import db_settings

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação do engine com configurações otimizadas
engine = create_engine(
    db_settings.database_url,
    poolclass=QueuePool,
    pool_size=db_settings.db_pool_size,
    max_overflow=db_settings.db_max_overflow,
    pool_pre_ping=True,
    pool_recycle=db_settings.db_pool_recycle,
    echo=db_settings.db_echo
)

# Configuração da fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Base para todos os modelos ORM
Base = declarative_base()

def get_database_session() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error(f"Erro na sessão do banco de dados: {e}")
        session.rollback()
        raise
    finally:
        session.close()

async def init_database():
    """
    Inicializa o banco de dados e cria as tabelas.
    Deve ser chamada no startup da aplicação.
    """
    try:
        logger.info("Inicializando conexão com o banco de dados...")
        
        # Verifica a conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"Conectado ao PostgreSQL: {version}")
        
        # Cria as tabelas
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas/verificadas com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        raise

async def close_database():
    """
    Fecha as conexões do banco de dados.
    Deve ser chamada no shutdown da aplicação.
    """
    try:
        engine.dispose()
        logger.info("Conexões do banco de dados fechadas")
    except Exception as e:
        logger.error(f"Erro ao fechar conexões do banco: {e}") 