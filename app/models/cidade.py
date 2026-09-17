from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Cidade(Base):
    """
    Representa uma cidade atendida pelo laticínio.
    Usa soft delete (campo `ativo`) em vez de exclusão física.
    """

    __tablename__ = "cidades"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    bairros: Mapped[list["Bairro"]] = relationship(back_populates="cidade")
