from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ItemPedidoBase(BaseModel):
    """
    Campos completos de um item de pedido, refletindo o model ItemPedido.
    Usado como base do schema de resposta. `pedido_id`, `preco_unitario`
    e `subtotal` são preenchidos pelo backend (nunca pela entrada do
    cliente) - ver ItemPedidoCreate.
    """

    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal


class ItemPedidoCreate(BaseModel):
    """
    Schema de entrada para o cliente solicitar um item dentro de um
    pedido.

    Contém apenas o que o cliente realmente escolhe: qual produto e em
    que quantidade. `pedido_id` é atribuído pelo backend a partir do
    pedido em criação; `preco_unitario` e `subtotal` serão calculados
    pelo pedido_service a partir do preço atual do produto no momento da
    compra - nunca informados pelo cliente.
    """

    produto_id: int
    quantidade: int


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
