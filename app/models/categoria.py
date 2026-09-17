from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Categoria(Base):
    """Categoria de produtos (ex: Leites, Queijos, Iogurtes). Usa soft delete."""

    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    produtos: Mapped[list["Produto"]] = relationship(back_populates="categoria")
