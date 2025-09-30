"""Contém o modelo ORM SQLAlchemy para a entidade Cliente."""

import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class Cliente(Base):
    """
    Modelo ORM para a entidade Cliente.

    Representa um cliente no banco de dados.
    """

    __tablename__ = "clientes"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), unique=True, index=True, nullable=False)
    telefone: str = Column(String(20), nullable=False)
    data_criacao: datetime.datetime = Column(DateTime, default=datetime.datetime.utcnow)


