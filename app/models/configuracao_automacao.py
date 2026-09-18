from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ConfiguracaoAutomacao(Base):
    __tablename__ = "configuracao_automacao"

    id: Mapped[int] = mapped_column(primary_key=True)
    ativa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )