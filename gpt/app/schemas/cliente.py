from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ClienteBase(BaseModel):
    """Campos comuns aos schemas de Cliente."""

    nome: str = Field(..., max_length=255)
    email: EmailStr
    telefone: str | None = Field(None, max_length=20)

    class Config:
        orm_mode = True


class ClienteCreate(ClienteBase):
    """Schema para criação de cliente."""

    # herda todos os campos obrigatórios de ClienteBase
    pass


class ClienteUpdate(BaseModel):
    """Schema para atualização parcial de cliente."""

    nome: str | None = Field(None, max_length=255)
    email: EmailStr | None = None
    telefone: str | None = Field(None, max_length=20)

    class Config:
        orm_mode = True


class ClienteRead(ClienteBase):
    """Schema para leitura de cliente, incluindo metadados."""

    id: int
    data_criacao: datetime
