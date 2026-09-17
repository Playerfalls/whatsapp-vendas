from pydantic import BaseModel, ConfigDict


class EnderecoBase(BaseModel):
    """Campos comuns de Endereco, compartilhados entre Create e Response."""

    cliente_id: int
    bairro_id: int
    cep: str
    logradouro: str
    numero: str
    complemento: str | None = None
    ponto_referencia: str | None = None


class EnderecoCreate(EnderecoBase):
    """Schema de entrada para criação de um endereço."""

    pass


class EnderecoUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de um endereço.
    Todos os campos são opcionais (PATCH semântico).
    """

    cliente_id: int | None = None
    bairro_id: int | None = None
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    ponto_referencia: str | None = None
    ativo: bool | None = None


class EnderecoResponse(EnderecoBase):
    """Schema de saída, refletindo o model Endereco."""

    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
