from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import StatusPedido


class Pedido(Base):
    """
    Representa um pedido feito por um cliente.

    `endereco_id` é uma referência OPCIONAL e apenas informativa ao
    endereço cadastrado que originou o pedido — não é a fonte de verdade
    sobre para onde o pedido foi entregue. Os campos de snapshot abaixo
    (logradouro_entrega, numero_entrega, etc.) são a cópia dos dados de
    entrega exatamente como estavam no momento da compra, preservando o
    histórico mesmo que o cliente edite ou remova o endereço depois.
    O mesmo vale para `taxa_entrega_aplicada`, que copia o valor de
    `Bairro.valor_taxa_entrega` no momento da criação do pedido.
    """

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"), nullable=False, index=True
    )
    endereco_id: Mapped[int | None] = mapped_column(
        ForeignKey("enderecos.id"), nullable=True, index=True
    )

    # Snapshot dos dados de entrega no momento da compra
    cep_entrega: Mapped[str] = mapped_column(String(9), nullable=False)
    logradouro_entrega: Mapped[str] = mapped_column(String(200), nullable=False)
    numero_entrega: Mapped[str] = mapped_column(String(20), nullable=False)
    complemento_entrega: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ponto_referencia_entrega: Mapped[str | None] = mapped_column(String(200), nullable=True)
    bairro_entrega_nome: Mapped[str] = mapped_column(String(120), nullable=False)
    cidade_entrega_nome: Mapped[str] = mapped_column(String(120), nullable=False)
    taxa_entrega_aplicada: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    status: Mapped[StatusPedido] = mapped_column(
        SAEnum(StatusPedido, native_enum=False, length=20),
        default=StatusPedido.NOVO,
        nullable=False,
        index=True,
    )
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    cliente: Mapped["Cliente"] = relationship(back_populates="pedidos")
    endereco: Mapped["Endereco | None"] = relationship(back_populates="pedidos")
    itens: Mapped[list["ItemPedido"]] = relationship(back_populates="pedido")
    pagamento: Mapped["Pagamento"] = relationship(
        back_populates="pedido", uselist=False
    )
    historico_status: Mapped[list["HistoricoStatusPedido"]] = relationship(
        back_populates="pedido"
    )
