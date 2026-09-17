from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.endereco import EnderecoCreate, EnderecoResponse, EnderecoUpdate
from app.services import endereco_service

router = APIRouter(prefix="/enderecos", tags=["Endereços"])


@router.post("", response_model=EnderecoResponse, status_code=status.HTTP_201_CREATED)
def criar_endereco(dados: EnderecoCreate, db: Session = Depends(get_db)):
    try:
        return endereco_service.criar_endereco(db, dados)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Não foi possível salvar o endereço. Verifique se o "
                "cliente e o bairro informados existem."
            ),
        )


@router.get("", response_model=list[EnderecoResponse])
def listar_enderecos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return endereco_service.listar_enderecos(db, skip=skip, limit=limit)


@router.get("/{endereco_id}", response_model=EnderecoResponse)
def obter_endereco(endereco_id: int, db: Session = Depends(get_db)):
    endereco = endereco_service.obter_endereco(db, endereco_id)
    if endereco is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado."
        )
    return endereco


@router.patch("/{endereco_id}", response_model=EnderecoResponse)
def atualizar_endereco(
    endereco_id: int, dados: EnderecoUpdate, db: Session = Depends(get_db)
):
    try:
        endereco = endereco_service.atualizar_endereco(db, endereco_id, dados)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Não foi possível atualizar o endereço. Verifique se o "
                "cliente e o bairro informados existem."
            ),
        )
    if endereco is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado."
        )
    return endereco


@router.delete("/{endereco_id}", response_model=EnderecoResponse)
def desativar_endereco(endereco_id: int, db: Session = Depends(get_db)):
    """
    Desativação lógica (soft delete): marca `ativo=False` em vez de
    remover o registro, preservando pedidos que já referenciam este
    endereço (via snapshot em Pedido, conforme já modelado).
    """
    endereco = endereco_service.desativar_endereco(db, endereco_id)
    if endereco is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado."
        )
    return endereco
