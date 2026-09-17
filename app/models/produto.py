from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Produto(Base):
    """
    Representa um produto do catálogo.

    `quantidade_estoque` substitui a antiga proposta de tabela `estoque`
    separada — para o MVP, um campo simples é suficiente (sem múltiplos
    depósitos, sem movimentações detalhadas). O comportamento de baixa
    automática de estoque ao criar um pedido fica para a fase de
    implementação de pedidos/estoque, não é tratado aqui.
    """

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantidade_estoque: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    categoria: Mapped["Categoria"] = relationship(back_populates="produtos")
    itens_pedido: Mapped[list["ItemPedido"]] = relationship(back_populates="produto")
