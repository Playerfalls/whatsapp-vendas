from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse
from app.services import pedido_service
from app.services.exceptions import EntidadeNaoEncontrada, ErroNegocio

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    """
    Cria um pedido. Todo o cálculo de preço, subtotal, taxa de entrega e
    valor total é responsabilidade de `pedido_service.criar_pedido` — a
    rota apenas repassa a entrada e traduz as exceções de negócio.
    """
    try:
        return pedido_service.criar_pedido(db, dados)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível salvar o pedido.",
        )


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return pedido_service.listar_pedidos(db, skip=skip, limit=limit)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = pedido_service.obter_pedido(db, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado."
        )
    return pedido
