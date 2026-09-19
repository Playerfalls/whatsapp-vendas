from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"

    id: Mapped[int] = mapped_column(primary_key=True)

    carrinho_id: Mapped[int] = mapped_column(
        ForeignKey("carrinhos.id"),
        nullable=False,
        index=True,
    )

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False,
        index=True,
    )

    quantidade: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    preco_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    carrinho: Mapped["Carrinho"] = relationship()

    produto: Mapped["Produto"] = relationship()