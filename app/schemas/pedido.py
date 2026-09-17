from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import StatusPedido


class PedidoBase(BaseModel):
    """
    Campos comuns de Pedido, compartilhados entre Create e Response.

    `endereco_id` é opcional e apenas informativo (mesmo comportamento do
    model). Os demais campos de entrega (`cep_entrega`,
    `logradouro_entrega` etc.) são o snapshot dos dados no momento da
    compra, conforme já definido na modelagem.
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


class PedidoCreate(PedidoBase):
    """
    Schema de entrada para criação de um pedido.

    `status` não é exposto aqui: o model define `NOVO` como valor padrão
    no momento da criação, então não faz sentido o cliente da API
    informá-lo na criação.
    """

    pass


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
