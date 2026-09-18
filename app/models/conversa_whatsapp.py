from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ConversaWhatsapp(Base):
    __tablename__ = "conversa_whatsapp"

    id: Mapped[int] = mapped_column(primary_key=True)

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="INICIO",
    )

    pedido_id: Mapped[int | None] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=True,
    )

    ultima_interacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )