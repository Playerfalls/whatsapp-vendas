from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


def criar_produto(db: Session, dados: ProdutoCreate) -> Produto:
    produto = Produto(**dados.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def listar_produtos(db: Session, skip: int = 0, limit: int = 100) -> list[Produto]:
    return db.query(Produto).offset(skip).limit(limit).all()


def obter_produto(db: Session, produto_id: int) -> Produto | None:
    return db.get(Produto, produto_id)


def atualizar_produto(
    db: Session, produto_id: int, dados: ProdutoUpdate
) -> Produto | None:
    produto = obter_produto(db, produto_id)
    if produto is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto


def desativar_produto(db: Session, produto_id: int) -> Produto | None:
    """
    Desativação lógica (soft delete) - nunca remove o registro fisicamente.
    Não mexe em `quantidade_estoque`: baixa de estoque é regra de fase futura.
    """
    produto = obter_produto(db, produto_id)
    if produto is None:
        return None
    produto.ativo = False
    db.commit()
    db.refresh(produto)
    return produto
