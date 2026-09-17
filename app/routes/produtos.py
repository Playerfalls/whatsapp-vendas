from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.services import produto_service
from app.services.exceptions import EntidadeNaoEncontrada, ErroNegocio

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    try:
        return produto_service.criar_produto(db, dados)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível salvar o produto.",
        )


@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return produto_service.listar_produtos(db, skip=skip, limit=limit)


@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = produto_service.obter_produto(db, produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado."
        )
    return produto


@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)
):
    try:
        produto = produto_service.atualizar_produto(db, produto_id, dados)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar o produto.",
        )
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado."
        )
    return produto


@router.delete("/{produto_id}", response_model=ProdutoResponse)
def desativar_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Desativação lógica (soft delete): marca `ativo=False` em vez de
    remover o registro, preservando itens de pedido que já referenciam
    este produto (que também guardam preço snapshot, independente disso).
    """
    produto = produto_service.desativar_produto(db, produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado."
        )
    return produto
