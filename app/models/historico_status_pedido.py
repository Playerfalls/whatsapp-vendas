from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import StatusPedido


class HistoricoStatusPedido(Base):
    """
    Registra cada mudança de status de um pedido ao longo do tempo,
    preservando o histórico completo (ex: NOVO -> PREPARANDO -> PRONTO).
    """

    __tablename__ = "historico_status_pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"), nullable=False, index=True
    )
    status_anterior: Mapped[StatusPedido | None] = mapped_column(
        SAEnum(StatusPedido, native_enum=False, length=20), nullable=True
    )
    status_novo: Mapped[StatusPedido] = mapped_column(
        SAEnum(StatusPedido, native_enum=False, length=20), nullable=False
    )
    data_alteracao: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    pedido: Mapped["Pedido"] = relationship(back_populates="historico_status")
