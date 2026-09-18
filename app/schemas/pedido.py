from datetime import datetime
from decimal import Decimal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from app.models.enums import FormaPagamento, StatusPagamento, StatusPedido
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoResponse
from app.schemas.pagamento import PagamentoResponse


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


class PedidoStatusUpdate(BaseModel):
    """
    Schema de entrada dedicado à alteração de status de um pedido
    (PATCH /pedidos/{pedido_id}/status). Contém somente o novo status -
    nenhum outro campo do pedido (id, cliente_id, endereco_id,
    valor_total, datas etc.) pode ser alterado por esta via.
    """

    status: StatusPedido


class PedidoDetalhadoResponse(BaseModel):
    """
    Schema de saída para a consulta detalhada de um pedido
    (GET /pedidos/{pedido_id}/detalhado), incluindo itens e pagamento.

    Reaproveita ItemPedidoResponse e PagamentoResponse já existentes,
    em vez de duplicar schemas. `total` é um alias de leitura para o
    campo `valor_total` do model Pedido - nenhum valor é recalculado, só
    exposto com outro nome de campo na resposta.

    Não há campo `subtotal`: o model Pedido não possui esse valor
    persistido (só existe `subtotal` por item, em ItemPedido), e este
    endpoint não deve calcular valores - apenas expor o que já está
    gravado no banco.
    """

    id: int
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
    total: Decimal = Field(validation_alias="valor_total")
    status: StatusPedido
    data_criacao: datetime
    data_atualizacao: datetime
    itens: list[ItemPedidoResponse]
    pagamento: PagamentoResponse

    model_config = ConfigDict(from_attributes=True)

class PedidoResumoResponse(BaseModel):
    """
    Schema de saída para a listagem operacional de pedidos
    (GET /pedidos).

    Contém somente os dados necessários para exibição da lista/painel.
    Informações completas de entrega, itens e pagamento ficam nos
    endpoints específicos do pedido.
    """

    id: int
    cliente_id: int
    cliente_nome: str = Field(validation_alias=AliasPath("cliente", "nome"))
    endereco_id: int | None = None
    bairro_entrega_nome: str
    cidade_entrega_nome: str
    valor_total: Decimal
    forma_pagamento: FormaPagamento = Field(
        validation_alias=AliasPath("pagamento", "forma_pagamento")
)
    status_pagamento: StatusPagamento = Field(
        validation_alias=AliasPath("pagamento", "status_pagamento")
)
    status: StatusPedido
    data_criacao: datetime
    data_atualizacao: datetime

    model_config = ConfigDict(from_attributes=True)

class PedidoContadoresResponse(BaseModel):
    novos: int
    preparando: int
    prontos: int
    em_rota: int
    finalizados: int
    cancelados: int
    retornados: int