from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ItemPedidoBase(BaseModel):
    """
    Campos comuns de ItemPedido, compartilhados entre Create e Response.

    `preco_unitario` e `subtotal` são os valores snapshot no momento da
    compra, exatamente como definidos no model — este schema não recalcula
    nem valida esses valores, apenas os transporta.
    """

    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal


class ItemPedidoCreate(ItemPedidoBase):
    """Schema de entrada para criação de um item de pedido."""

    pass


class ItemPedidoUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de um item de pedido.
    Todos os campos são opcionais (PATCH semântico).
    """

    pedido_id: int | None = None
    produto_id: int | None = None
    quantidade: int | None = None
    preco_unitario: Decimal | None = None
    subtotal: Decimal | None = None


class ItemPedidoResponse(ItemPedidoBase):
    """Schema de saída, refletindo o model ItemPedido."""

    id: int

    model_config = ConfigDict(from_attributes=True)
