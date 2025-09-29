import os
from typing import Optional
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    """
    Configurações do banco de dados usando Pydantic para validação.
    """
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "12345678"
    db_name: str = "db"
    db_echo: bool = False
    
    # Pool de conexões
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_recycle: int = 300
    
    class Config:
        env_prefix = "DB_"
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        """
        Constrói a URL de conexão do PostgreSQL.
        """
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

# Instância global das configurações
db_settings = DatabaseSettings() 