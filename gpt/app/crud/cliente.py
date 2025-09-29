from typing import List, Sequence

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.cliente import Cliente
from app.schemas.cliente import (
    ClienteCreate,
    ClienteRead,
    ClienteUpdate,
)


class CRUDCliente:
    """Camada de acesso a dados (CRUD) para Cliente."""

    def _raise_not_found(self, cliente_id: int) -> None:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente id={cliente_id} não encontrado.",
        )

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------
    def create(self, db: Session, obj_in: ClienteCreate) -> ClienteRead:
        """Cria um novo cliente e retorna dados conforme *ClienteRead*."""
        cliente = Cliente(**obj_in.dict())
        db.add(cliente)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            # Trata email duplicado
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já cadastrado.",
            ) from exc

        db.refresh(cliente)
        return ClienteRead.from_orm(cliente)

    def get_by_id(self, db: Session, cliente_id: int) -> ClienteRead:
        """Busca cliente pelo id."""
        cliente: Cliente | None = db.get(Cliente, cliente_id)
        if not cliente:
            self._raise_not_found(cliente_id)
        return ClienteRead.from_orm(cliente)

    def list(self, db: Session) -> List[ClienteRead]:
        """Lista todos os clientes."""
        clientes: Sequence[Cliente] = db.query(Cliente).all()
        return [ClienteRead.from_orm(c) for c in clientes]

    def update(
        self, db: Session, cliente_id: int, obj_in: ClienteUpdate
    ) -> ClienteRead:
        """Atualiza cliente parcialmente com campos enviados."""
        cliente: Cliente | None = db.get(Cliente, cliente_id)
        if not cliente:
            self._raise_not_found(cliente_id)

        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(cliente, field, value)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            # Email duplicado
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já cadastrado.",
            ) from exc

        db.refresh(cliente)
        return ClienteRead.from_orm(cliente)

    def delete(self, db: Session, cliente_id: int) -> None:
        """Remove cliente pelo id."""
        cliente: Cliente | None = db.get(Cliente, cliente_id)
        if not cliente:
            self._raise_not_found(cliente_id)
        db.delete(cliente)
        db.commit()
