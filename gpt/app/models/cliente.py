from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

from app.db.base import Base


class Cliente(Base):
    """ORM model representing a client (cliente)."""

    __tablename__ = "clientes"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(255), nullable=False)
    email: str = Column(String(255), nullable=False, unique=True, index=True)
    telefone: str | None = Column(String(20), nullable=True)
    data_criacao: datetime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_clientes_email"),
    )

    # ---------------------------------------------------------------------
    # Magic methods
    # ---------------------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Cliente id={self.id} nome={self.nome!r} email={self.email!r} "
            f"telefone={self.telefone!r} data_criacao={self.data_criacao}>"
        )
