from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import FormaPagamento, StatusPedido
from app.schemas.item_pedido import ItemPedidoCreate


class PedidoBase(BaseModel):
    """
    Campos completos de um pedido, refletindo o model Pedido. Usado como
    base do schema de resposta.

    Os campos de entrega (`cep_entrega`, `logradouro_entrega` etc.) e
    `taxa_entrega_aplicada`/`valor_total` são o snapshot calculado pelo
    backend no momento da criação — nunca informados diretamente pelo
    cliente (ver PedidoCreate).
    """

    cliente_id: int
    endereco_id: int | None = None
    cep_entrega: str
    logradouro_entrega: str
    numero_entrega: str
    complemento_entrega: str | None = None
    ponto_referencia_entrega: str | None = None
    bairro_entrega_nome: str
    cidade_entrega_nome: str
    taxa_entrega_aplicada: Decimal
    valor_total: Decimal


class PedidoCreate(BaseModel):
    """
    Schema de entrada para o cliente solicitar um pedido.

    Contém apenas o que o cliente realmente escolhe: para qual cliente,
    qual endereço cadastrado (usado pelo pedido_service para copiar o
    snapshot de entrega e a taxa vigente do bairro), a forma de
    pagamento escolhida e quais itens deseja. Todos os campos de
    entrega, a taxa aplicada e o valor total serão calculados pelo
    backend a partir de `endereco_id` e dos itens - nunca informados
    diretamente pelo cliente.
    """

    cliente_id: int
    endereco_id: int
    forma_pagamento: FormaPagamento
    itens: list[ItemPedidoCreate]


class PedidoUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de um pedido.
    Todos os campos são opcionais (PATCH semântico), incluindo `status`,
    que aqui pode ser atualizado (ex: mudança de NOVO para PREPARANDO).
    """

    cliente_id: int | None = None
    endereco_id: int | None = None
    cep_entrega: str | None = None
    logradouro_entrega: str | None = None
    numero_entrega: str | None = None
    complemento_entrega: str | None = None
    ponto_referencia_entrega: str | None = None
    bairro_entrega_nome: str | None = None
    cidade_entrega_nome: str | None = None
    taxa_entrega_aplicada: Decimal | None = None
    valor_total: Decimal | None = None
    status: StatusPedido | None = None


class PedidoResponse(PedidoBase):
    """Schema de saída, refletindo o model Pedido."""

    id: int
    status: StatusPedido
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = ConfigDict(from_attributes=True)
