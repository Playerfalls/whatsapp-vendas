from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.cidade import CidadeCreate, CidadeResponse, CidadeUpdate
from app.services import cidade_service
from app.services.exceptions import ConflitoDados, ErroNegocio

router = APIRouter(prefix="/cidades", tags=["Cidades"])


@router.post("", response_model=CidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_cidade(dados: CidadeCreate, db: Session = Depends(get_db)):
    try:
        return cidade_service.criar_cidade(db, dados)
    except ConflitoDados as erro:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível salvar a cidade.",
        )


@router.get("", response_model=list[CidadeResponse])
def listar_cidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cidade_service.listar_cidades(db, skip=skip, limit=limit)


@router.get("/{cidade_id}", response_model=CidadeResponse)
def obter_cidade(cidade_id: int, db: Session = Depends(get_db)):
    cidade = cidade_service.obter_cidade(db, cidade_id)
    if cidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada."
        )
    return cidade


@router.patch("/{cidade_id}", response_model=CidadeResponse)
def atualizar_cidade(cidade_id: int, dados: CidadeUpdate, db: Session = Depends(get_db)):
    try:
        cidade = cidade_service.atualizar_cidade(db, cidade_id, dados)
    except ConflitoDados as erro:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)
    if cidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada."
        )
    return cidade


@router.delete("/{cidade_id}", response_model=CidadeResponse)
def desativar_cidade(cidade_id: int, db: Session = Depends(get_db)):
    """
    Desativação lógica (soft delete): marca `ativo=False` em vez de
    remover o registro, preservando bairros/endereços/pedidos que já
    referenciam esta cidade.
    """
    cidade = cidade_service.desativar_cidade(db, cidade_id)
    if cidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada."
        )
    return cidade
