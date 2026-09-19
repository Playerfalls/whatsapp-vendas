from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Carrinho(Base):
    __tablename__ = "carrinhos"

    id: Mapped[int] = mapped_column(primary_key=True)

    conversa_id: Mapped[int] = mapped_column(
        ForeignKey("conversa_whatsapp.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    conversa: Mapped["ConversaWhatsapp"] = relationship()