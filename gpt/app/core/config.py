from functools import lru_cache
from typing import Optional

from pydantic import PostgresDsn, validator, BaseSettings

class Settings(BaseSettings):
    """
    Centraliza configurações vindas de variáveis de ambiente ou arquivo .env.
    """
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'db'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = '12345678'

    # Permite apontar para DATABASE_URL pronto (ex.: render, heroku...)
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # Ativa log das queries (útil em dev)
    ECHO_SQL: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    # Monta a URL caso não tenha sido passada completa
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_conn(cls, v: Optional[str], values) -> str:
        if isinstance(v, str) and v:
            return v

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


@lru_cache()
def get_settings() -> Settings:
    """
    Usa lru_cache para evitar recriar Settings a cada import.
    """
    return Settings() 