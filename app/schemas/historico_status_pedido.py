from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import StatusPedido


class HistoricoStatusPedidoResponse(BaseModel):
    """
    Schema de saída para um registro de histórico de status de pedido.

    Somente leitura: não existe schema de entrada para esta entidade,
    pois o cliente da API nunca cria ou edita registros de histórico
    diretamente - eles são gerados automaticamente por
    `pedido_service.atualizar_status_pedido`.
    """

    id: int
    pedido_id: int
    status_anterior: StatusPedido | None = None
    status_novo: StatusPedido
    data_alteracao: datetime

    model_config = ConfigDict(from_attributes=True)
