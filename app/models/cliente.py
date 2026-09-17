from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Cliente(Base):
    """
    Representa um cliente identificado pelo WhatsApp.

    `telefone` é único e é o identificador principal do cliente no fluxo
    de atendimento. Regra de negócio importante (a ser aplicada pela
    aplicação, não pelo banco): o telefone deve ser normalizado para um
    formato único (ex: apenas dígitos, com DDI/DDD) ANTES de ser
    persistido, para que o mesmo número não seja cadastrado em formatos
    diferentes. Essa normalização será implementada na camada de
    services, que ainda não existe nesta fase.
    """

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    enderecos: Mapped[list["Endereco"]] = relationship(back_populates="cliente")
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")
