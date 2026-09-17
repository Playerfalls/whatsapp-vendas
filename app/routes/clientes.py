from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services import cliente_service
from app.services.exceptions import ConflitoDados, EntidadeNaoEncontrada, ErroNegocio

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return cliente_service.criar_cliente(db, dados)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)
    except ConflitoDados as erro:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível salvar o cliente.",
        )


@router.get("", response_model=list[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cliente_service.listar_clientes(db, skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = cliente_service.obter_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int, dados: ClienteUpdate, db: Session = Depends(get_db)
):
    try:
        cliente = cliente_service.atualizar_cliente(db, cliente_id, dados)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)
    except ConflitoDados as erro:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar o cliente.",
        )
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
    return cliente


@router.delete("/{cliente_id}", response_model=ClienteResponse)
def desativar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Desativação lógica (soft delete): marca `ativo=False` em vez de
    remover o registro, preservando histórico e relacionamentos (ex:
    pedidos já feitos por este cliente).
    """
    cliente = cliente_service.desativar_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
    return cliente
