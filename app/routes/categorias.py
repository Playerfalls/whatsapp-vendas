from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from app.services import categoria_service

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(dados: CategoriaCreate, db: Session = Depends(get_db)):
    try:
        return categoria_service.criar_categoria(db, dados)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível salvar a categoria.",
        )


@router.get("", response_model=list[CategoriaResponse])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return categoria_service.listar_categorias(db, skip=skip, limit=limit)


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = categoria_service.obter_categoria(db, categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada."
        )
    return categoria


@router.patch("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(
    categoria_id: int, dados: CategoriaUpdate, db: Session = Depends(get_db)
):
    categoria = categoria_service.atualizar_categoria(db, categoria_id, dados)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada."
        )
    return categoria


@router.delete("/{categoria_id}", response_model=CategoriaResponse)
def desativar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Desativação lógica (soft delete): marca `ativo=False` em vez de
    remover o registro, preservando produtos/itens de pedido que já
    referenciam esta categoria.
    """
    categoria = categoria_service.desativar_categoria(db, categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada."
        )
    return categoria
