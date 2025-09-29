"""
Modelos ORM SQLAlchemy para a aplicação.
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.schema import UniqueConstraint
from database_config import Base
from datetime import datetime
from typing import Optional


class Cliente(Base):
    """
    Modelo ORM para a entidade Cliente.
    
    Representa um cliente do sistema com informações básicas
    como nome, email, telefone e data de criação.
    """
    __tablename__ = "clientes"
    
    # Chave primária
    id: int = Column(
        Integer, 
        primary_key=True, 
        index=True,
        autoincrement=True,
        doc="Identificador único do cliente"
    )
    
    # Campos obrigatórios
    nome: str = Column(
        String(255), 
        nullable=False,
        doc="Nome completo do cliente"
    )
    
    email: str = Column(
        String(255), 
        nullable=False, 
        unique=True,
        index=True,
        doc="Email único do cliente"
    )
    
    telefone: str = Column(
        String(20), 
        nullable=False,
        doc="Telefone de contato do cliente"
    )
    
    # Campo de auditoria
    data_criacao: datetime = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        doc="Data e hora de criação do registro"
    )
    
    # Constraints adicionais
    __table_args__ = (
        UniqueConstraint('email', name='uq_cliente_email'),
    )
    
    def __repr__(self) -> str:
        """
        Representação string do objeto Cliente.
        
        Returns:
            str: Representação formatada do cliente
        """
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}')>"
    
    def __str__(self) -> str:
        """
        String amigável do objeto Cliente.
        
        Returns:
            str: Nome do cliente
        """
        return self.nome
