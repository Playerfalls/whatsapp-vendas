from pydantic import BaseModel, ConfigDict


class CidadeBase(BaseModel):
    """Campos comuns de Cidade, compartilhados entre Create e Response."""

    nome: str


class CidadeCreate(CidadeBase):
    """Schema de entrada para criação de uma cidade."""

    pass


class CidadeUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de uma cidade.
    Todos os campos são opcionais (PATCH semântico).
    """

    nome: str | None = None
    ativo: bool | None = None


class CidadeResponse(CidadeBase):
    """Schema de saída, refletindo o model Cidade."""

    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
