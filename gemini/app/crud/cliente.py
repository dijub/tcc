"""Contém as operações de CRUD para a entidade Cliente."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def create_cliente(db: Session, cliente: ClienteCreate) -> Cliente:
    """
    Cria um novo cliente no banco de dados.

    Args:
        db: A sessão do banco de dados.
        cliente: Os dados do cliente a serem criados.

    Returns:
        O cliente recém-criado.
    """
    db_cliente = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone,
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def get_cliente(db: Session, cliente_id: int) -> Optional[Cliente]:
    """
    Busca um cliente pelo seu ID.

    Args:
        db: A sessão do banco de dados.
        cliente_id: O ID do cliente a ser buscado.

    Returns:
        O cliente, se encontrado, ou None.
    """
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def get_cliente_by_email(db: Session, email: str) -> Optional[Cliente]:
    """
    Busca um cliente pelo seu email.

    Args:
        db: A sessão do banco de dados.
        email: O email do cliente a ser buscado.

    Returns:
        O cliente, se encontrado, ou None.
    """
    return db.query(Cliente).filter(Cliente.email == email).first()


def get_clientes(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
    """
    Lista todos os clientes com paginação.

    Args:
        db: A sessão do banco de dados.
        skip: O número de registros a pular.
        limit: O número máximo de registros a retornar.

    Returns:
        Uma lista de clientes.
    """
    return db.query(Cliente).offset(skip).limit(limit).all()


def update_cliente(db: Session, cliente_id: int, cliente_update: ClienteUpdate) -> Optional[Cliente]:
    """
    Atualiza um cliente existente.

    Args:
        db: A sessão do banco de dados.
        cliente_id: O ID do cliente a ser atualizado.
        cliente_update: Os dados do cliente a serem atualizados.

    Returns:
        O cliente atualizado, se encontrado, ou None.
    """
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None

    update_data = cliente_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)

    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, cliente_id: int) -> Optional[Cliente]:
    """
    Deleta um cliente existente.

    Args:
        db: A sessão do banco de dados.
        cliente_id: O ID do cliente a ser deletado.

    Returns:
        O cliente deletado, se encontrado, ou None.
    """
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None

    db.delete(db_cliente)
    db.commit()
    return db_cliente
