from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.cliente import (
    ClienteCreate,
    ClienteRead,
    ClienteUpdate,
)
from app.crud import cliente_crud

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def create_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_in: ClienteCreate,
) -> ClienteRead:
    """Cria um novo cliente."""
    return cliente_crud.create(db, cliente_in)


@router.get("", response_model=List[ClienteRead])
def list_clientes(*, db: Session = Depends(get_db)) -> List[ClienteRead]:
    """Retorna lista de clientes."""
    return cliente_crud.list(db)


@router.get("/{cliente_id}", response_model=ClienteRead)
def get_cliente(
    *, db: Session = Depends(get_db), cliente_id: int
) -> ClienteRead:
    """Retorna cliente por id."""
    return cliente_crud.get_by_id(db, cliente_id)


@router.put("/{cliente_id}", response_model=ClienteRead)
def update_cliente(
    *,
    db: Session = Depends(get_db),
    cliente_id: int,
    cliente_in: ClienteUpdate,
) -> ClienteRead:
    """Atualiza cliente existente."""
    return cliente_crud.update(db, cliente_id, cliente_in)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(*, db: Session = Depends(get_db), cliente_id: int) -> Response:
    """Remove cliente."""
    cliente_crud.delete(db, cliente_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
