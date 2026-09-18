from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversaWhatsappResponse(BaseModel):
    id: int
    telefone: str
    estado: str
    pedido_id: int | None = None
    ultima_interacao: datetime

    model_config = ConfigDict(from_attributes=True)