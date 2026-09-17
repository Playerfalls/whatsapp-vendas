from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Endereco(Base):
    """
    Endereço cadastrado por um cliente.

    Importante: pedidos NÃO dependem exclusivamente deste registro para
    saber para onde foram entregues — eles gravam uma cópia (snapshot)
    dos dados de entrega no momento da compra (ver Pedido). Este model
    representa apenas os endereços atualmente cadastrados/editáveis pelo
    cliente.
    """

    __tablename__ = "enderecos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"), nullable=False, index=True
    )
    bairro_id: Mapped[int] = mapped_column(
        ForeignKey("bairros.id"), nullable=False, index=True
    )
    cep: Mapped[str] = mapped_column(String(9), nullable=False)
    logradouro: Mapped[str] = mapped_column(String(200), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    complemento: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ponto_referencia: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="enderecos")
    bairro: Mapped["Bairro"] = relationship(back_populates="enderecos")
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="endereco")
