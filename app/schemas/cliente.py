from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    """
    Campos comuns de Cliente, compartilhados entre Create e Response.

    Observação: a normalização do telefone e do CPF/CNPJ é responsabilidade
    da aplicação/service, não deste schema.
    """

    nome: str
    telefone: str
    cpf_cnpj: str | None = None


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
    cpf_cnpj: str | None = None

class ClienteResponse(ClienteBase):
    """Schema de saída, refletindo o model Cliente."""

    id: int
    data_cadastro: datetime
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
