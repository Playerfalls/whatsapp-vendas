from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProdutoBase(BaseModel):
    """Campos comuns de Produto, compartilhados entre Create e Response."""

    categoria_id: int
    nome: str
    descricao: str | None = None
    preco: Decimal
    quantidade_estoque: int


class ProdutoCreate(ProdutoBase):
    """Schema de entrada para criação de um produto."""

    pass


class ProdutoUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de um produto.
    Todos os campos são opcionais (PATCH semântico).
    """

    categoria_id: int | None = None
    nome: str | None = None
    descricao: str | None = None
    preco: Decimal | None = None
    quantidade_estoque: int | None = None
    ativo: bool | None = None


class ProdutoResponse(ProdutoBase):
    """Schema de saída, refletindo o model Produto."""

    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
