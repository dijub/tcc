"""Contém as rotas da API para a entidade Cliente."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.cliente import (
    create_cliente,
    delete_cliente,
    get_cliente,
    get_cliente_by_email,
    get_clientes,
    update_cliente,
)
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=ClienteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo cliente",
)
def create_new_cliente(cliente_in: ClienteCreate, db: Session = Depends(get_db)):
    """
    Cria um novo cliente no sistema.

    Verifica se já existe um cliente com o mesmo e-mail.
    """
    db_cliente = get_cliente_by_email(db, email=cliente_in.email)
    if db_cliente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um cliente com este e-mail já existe.",
        )
    return create_cliente(db=db, cliente=cliente_in)


@router.get(
    "/",
    response_model=List[ClienteRead],
    summary="Lista todos os clientes",
)
def read_all_clientes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de clientes com paginação.
    """
    return get_clientes(db, skip=skip, limit=limit)


@router.get(
    "/{cliente_id}",
    response_model=ClienteRead,
    summary="Busca um cliente pelo ID",
)
def read_one_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Retorna um cliente específico com base no ID.
    """
    db_cliente = get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )
    return db_cliente


@router.put(
    "/{cliente_id}",
    response_model=ClienteRead,
    summary="Atualiza um cliente",
)
def update_one_cliente(
    cliente_id: int, cliente_in: ClienteUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um cliente existente.
    """
    db_cliente = update_cliente(db, cliente_id=cliente_id, cliente_update=cliente_in)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )
    return db_cliente


@router.delete(
    "/{cliente_id}",
    response_model=ClienteRead,
    summary="Deleta um cliente",
)
def delete_one_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Remove um cliente do sistema.
    """
    db_cliente = delete_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )
    return db_cliente
