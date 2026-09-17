from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BairroBase(BaseModel):
    """Campos comuns de Bairro, compartilhados entre Create e Response."""

    cidade_id: int
    nome: str
    valor_taxa_entrega: Decimal


class BairroCreate(BairroBase):
    """Schema de entrada para criação de um bairro."""

    pass


class BairroUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de um bairro.
    Todos os campos são opcionais (PATCH semântico).
    """

    cidade_id: int | None = None
    nome: str | None = None
    valor_taxa_entrega: Decimal | None = None
    ativo: bool | None = None


class BairroResponse(BairroBase):
    """Schema de saída, refletindo o model Bairro."""

    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
