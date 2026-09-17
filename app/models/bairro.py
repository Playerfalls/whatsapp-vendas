from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Bairro(Base):
    """
    Representa um bairro dentro de uma cidade.

    `valor_taxa_entrega` é o valor vigente da taxa de entrega para o bairro.
    Quando um pedido é criado, esse valor é copiado para o próprio pedido
    (campo `taxa_entrega_aplicada` em Pedido), preservando o histórico
    mesmo que a taxa do bairro seja alterada depois.
    """

    __tablename__ = "bairros"

    id: Mapped[int] = mapped_column(primary_key=True)
    cidade_id: Mapped[int] = mapped_column(
        ForeignKey("cidades.id"), nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    valor_taxa_entrega: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cidade: Mapped["Cidade"] = relationship(back_populates="bairros")
    enderecos: Mapped[list["Endereco"]] = relationship(back_populates="bairro")
