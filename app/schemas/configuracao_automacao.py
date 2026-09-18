from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConfiguracaoAutomacaoResponse(BaseModel):
    id: int
    ativa: bool
    data_atualizacao: datetime

    model_config = ConfigDict(from_attributes=True)


class ConfiguracaoAutomacaoUpdate(BaseModel):
    ativa: bool