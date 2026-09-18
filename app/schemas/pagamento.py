from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import FormaPagamento, StatusPagamento


class PagamentoBase(BaseModel):
    """Campos comuns de Pagamento, compartilhados entre Create e Response."""

    pedido_id: int
    forma_pagamento: FormaPagamento
    valor: Decimal


class PagamentoCreate(PagamentoBase):
    """
    Schema de entrada para criação de um pagamento.

    `status_pagamento` não é exposto aqui: o model define `PENDENTE` como
    valor padrão no momento da criação.
    """

    pass


class PagamentoUpdate(BaseModel):
    forma_pagamento: FormaPagamento | None = None
    status_pagamento: StatusPagamento | None = None


class PagamentoResponse(PagamentoBase):
    """Schema de saída, refletindo o model Pagamento."""

    id: int
    status_pagamento: StatusPagamento
    data_pagamento: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
