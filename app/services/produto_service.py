from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.services.exceptions import EntidadeNaoEncontrada, ErroNegocio


def _validar_nome(nome: str) -> str:
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ErroNegocio("Nome do produto é obrigatório.")
    return nome_limpo


def _validar_preco(preco: Decimal) -> Decimal:
    if preco < 0:
        raise ErroNegocio("O preço do produto não pode ser negativo.")
    return preco


def _validar_estoque(quantidade_estoque: int) -> int:
    if quantidade_estoque < 0:
        raise ErroNegocio("A quantidade em estoque não pode ser negativa.")
    return quantidade_estoque


def _validar_categoria(db: Session, categoria_id: int) -> None:
    categoria = db.get(Categoria, categoria_id)
    if categoria is None:
        raise EntidadeNaoEncontrada("Categoria informada não existe.")
    if not categoria.ativo:
        raise ErroNegocio("Não é possível usar uma categoria inativa para o produto.")


def criar_produto(db: Session, dados: ProdutoCreate) -> Produto:
    _validar_categoria(db, dados.categoria_id)
    nome = _validar_nome(dados.nome)
    preco = _validar_preco(dados.preco)
    quantidade_estoque = _validar_estoque(dados.quantidade_estoque)

    produto = Produto(
        categoria_id=dados.categoria_id,
        nome=nome,
        descricao=dados.descricao,
        preco=preco,
        quantidade_estoque=quantidade_estoque,
    )
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

    valores = dados.model_dump(exclude_unset=True)
    if "categoria_id" in valores:
        _validar_categoria(db, valores["categoria_id"])
    if "nome" in valores:
        valores["nome"] = _validar_nome(valores["nome"])
    if "preco" in valores:
        valores["preco"] = _validar_preco(valores["preco"])
    if "quantidade_estoque" in valores:
        valores["quantidade_estoque"] = _validar_estoque(valores["quantidade_estoque"])

    for campo, valor in valores.items():
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
