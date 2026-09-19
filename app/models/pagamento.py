from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import FormaPagamento, StatusPagamento


class Pagamento(Base):
    """
    Representa o registro de pagamento de um pedido (relação 1:1 com
    Pedido, garantida pelo `unique=True` em `pedido_id`).

    Nesta fase não há gateway nem processamento real de pagamento — este
    model apenas registra a forma escolhida e o status, atualizados
    manualmente. `status_pagamento` é independente de `Pedido.status`.
    """

    __tablename__ = "pagamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"), nullable=False, unique=True
    )
    forma_pagamento: Mapped[FormaPagamento] = mapped_column(
        SAEnum(FormaPagamento, native_enum=False, length=20), nullable=False
    )
    status_pagamento: Mapped[StatusPagamento] = mapped_column(
        SAEnum(StatusPagamento, native_enum=False, length=20),
        default=StatusPagamento.PENDENTE,
        nullable=False,
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    data_pagamento: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    pedido: Mapped["Pedido"] = relationship(back_populates="pagamento")

    cobranca_pix: Mapped["CobrancaPix | None"] = relationship(
        back_populates="pagamento",
        uselist=False,
    )
