"""
Schemas Pydantic para validação de dados da aplicação.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ClienteBase(BaseModel):
    """
    Schema base para Cliente com campos comuns.
    """
    nome: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Nome completo do cliente",
        example="João Silva"
    )
    email: EmailStr = Field(
        ...,
        description="Email válido do cliente",
        example="joao.silva@email.com"
    )
    telefone: str = Field(
        ...,
        min_length=8,
        max_length=20,
        pattern=r'^[\d\s\-\(\)\+]+$',
        description="Telefone de contato (apenas números, espaços, hífens, parênteses e +)",
        example="(11) 99999-9999"
    )


class ClienteCreate(ClienteBase):
    """
    Schema para criação de Cliente.
    
    Contém todos os campos obrigatórios para criar um novo cliente.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "telefone": "(11) 99999-9999"
            }
        }
    )


class ClienteUpdate(BaseModel):
    """
    Schema para atualização parcial de Cliente.
    
    Todos os campos são opcionais para permitir atualizações parciais.
    """
    nome: Optional[str] = Field(
        None,
        min_length=2,
        max_length=255,
        description="Nome completo do cliente",
        example="João Silva Santos"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Email válido do cliente",
        example="joao.santos@email.com"
    )
    telefone: Optional[str] = Field(
        None,
        min_length=8,
        max_length=20,
        pattern=r'^[\d\s\-\(\)\+]+$',
        description="Telefone de contato (apenas números, espaços, hífens, parênteses e +)",
        example="(11) 88888-8888"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "João Silva Santos",
                "email": "joao.santos@email.com",
                "telefone": "(11) 88888-8888"
            }
        }
    )


class ClienteRead(ClienteBase):
    """
    Schema para leitura de Cliente.
    
    Inclui todos os campos do modelo, incluindo id e data_criacao.
    """
    id: int = Field(
        ...,
        description="Identificador único do cliente",
        example=1
    )
    data_criacao: datetime = Field(
        ...,
        description="Data e hora de criação do cliente",
        example="2023-12-01T10:30:00Z"
    )
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "telefone": "(11) 99999-9999",
                "data_criacao": "2023-12-01T10:30:00Z"
            }
        }
    )


class ClienteInDB(ClienteRead):
    """
    Schema para Cliente como armazenado no banco de dados.
    
    Herda de ClienteRead mas pode incluir campos adicionais
    específicos para operações internas do banco.
    """
    pass
