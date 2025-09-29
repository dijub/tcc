"""Contém os schemas Pydantic para a entidade Cliente."""

import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    """Schema base para Cliente com campos comuns."""

    nome: str
    email: EmailStr
    telefone: str


class ClienteCreate(ClienteBase):
    """Schema para a criação de um novo cliente."""

    pass


class ClienteUpdate(BaseModel):
    """Schema para a atualização de um cliente existente."""

    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None


class ClienteRead(ClienteBase):
    """Schema para a leitura de dados de um cliente."""

    id: int
    data_criacao: datetime.datetime

    class Config:
        """Configuração do schema Pydantic."""

        orm_mode = True
