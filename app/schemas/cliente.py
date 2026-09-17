from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    """
    Campos comuns de Cliente, compartilhados entre Create e Response.

    Observação: a normalização do telefone (mesma regra já documentada
    no model Cliente) é responsabilidade da aplicação/service, não deste
    schema — o schema apenas valida que é uma string.
    """

    nome: str
    telefone: str


class ClienteCreate(ClienteBase):
    """Schema de entrada para criação de um cliente."""

    pass


class ClienteUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de um cliente.
    Todos os campos são opcionais (PATCH semântico).
    """

    nome: str | None = None
    telefone: str | None = None
    ativo: bool | None = None


class ClienteResponse(ClienteBase):
    """Schema de saída, refletindo o model Cliente."""

    id: int
    data_cadastro: datetime
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
