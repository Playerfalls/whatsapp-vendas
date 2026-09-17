from pydantic import BaseModel, ConfigDict


class CategoriaBase(BaseModel):
    """Campos comuns de Categoria, compartilhados entre Create e Response."""

    nome: str


class CategoriaCreate(CategoriaBase):
    """Schema de entrada para criação de uma categoria."""

    pass


class CategoriaUpdate(BaseModel):
    """
    Schema de entrada para atualização parcial de uma categoria.
    Todos os campos são opcionais (PATCH semântico).
    """

    nome: str | None = None
    ativo: bool | None = None


class CategoriaResponse(CategoriaBase):
    """Schema de saída, refletindo o model Categoria."""

    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
