from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.bairro import BairroCreate, BairroResponse, BairroUpdate
from app.services import bairro_service

router = APIRouter(prefix="/bairros", tags=["Bairros"])


@router.post("", response_model=BairroResponse, status_code=status.HTTP_201_CREATED)
def criar_bairro(dados: BairroCreate, db: Session = Depends(get_db)):
    try:
        return bairro_service.criar_bairro(db, dados)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível salvar o bairro. Verifique se a cidade informada existe.",
        )


@router.get("", response_model=list[BairroResponse])
def listar_bairros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return bairro_service.listar_bairros(db, skip=skip, limit=limit)


@router.get("/{bairro_id}", response_model=BairroResponse)
def obter_bairro(bairro_id: int, db: Session = Depends(get_db)):
    bairro = bairro_service.obter_bairro(db, bairro_id)
    if bairro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bairro não encontrado."
        )
    return bairro


@router.patch("/{bairro_id}", response_model=BairroResponse)
def atualizar_bairro(bairro_id: int, dados: BairroUpdate, db: Session = Depends(get_db)):
    try:
        bairro = bairro_service.atualizar_bairro(db, bairro_id, dados)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar o bairro. Verifique se a cidade informada existe.",
        )
    if bairro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bairro não encontrado."
        )
    return bairro


@router.delete("/{bairro_id}", response_model=BairroResponse)
def desativar_bairro(bairro_id: int, db: Session = Depends(get_db)):
    """
    Desativação lógica (soft delete): marca `ativo=False` em vez de
    remover o registro, preservando endereços/pedidos que já referenciam
    este bairro.
    """
    bairro = bairro_service.desativar_bairro(db, bairro_id)
    if bairro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bairro não encontrado."
        )
    return bairro
