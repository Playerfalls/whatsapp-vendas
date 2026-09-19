from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Cliente(Base):
    """
    Representa um cliente identificado pelo WhatsApp.

    `telefone` é o identificador principal do cliente no fluxo de
    atendimento. A unicidade do telefone é garantida na camada de
    service (app/services/cliente_service.py), considerando apenas
    clientes ATIVOS — por isso não há `unique=True` no banco: um
    telefone pode se repetir entre um cliente inativo (soft delete) e um
    novo cliente ativo, mas nunca entre dois clientes ativos ao mesmo
    tempo. A normalização (mantendo apenas dígitos) também é feita na
    camada de service, antes da persistência.
    """

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    cpf_cnpj: Mapped[str | None] = mapped_column(
    String(14),
    nullable=True,
)
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    enderecos: Mapped[list["Endereco"]] = relationship(back_populates="cliente")
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")
