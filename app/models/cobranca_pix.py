from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CobrancaPix(Base):
    __tablename__ = "cobrancas_pix"

    id: Mapped[int] = mapped_column(primary_key=True)

    pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("pagamentos.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    asaas_payment_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    pix_payload: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    pix_expira_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status_externo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    pagamento: Mapped["Pagamento"] = relationship(
        back_populates="cobranca_pix",
    )