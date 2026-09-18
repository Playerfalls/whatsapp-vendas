from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.historico_status_pedido import HistoricoStatusPedidoResponse
from app.schemas.pedido import (
    PedidoCreate,
    PedidoDetalhadoResponse,
    PedidoResponse,
    PedidoStatusUpdate,
)
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


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def atualizar_status_pedido(
    pedido_id: int, dados: PedidoStatusUpdate, db: Session = Depends(get_db)
):
    """
    Altera o status do pedido e registra a mudança em
    HistoricoStatusPedido (feito por `pedido_service.atualizar_status_pedido`,
    na mesma transação).
    """
    try:
        return pedido_service.atualizar_status_pedido(db, pedido_id, dados.status)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)
    except ErroNegocio as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro.mensagem)


@router.get(
    "/{pedido_id}/historico", response_model=list[HistoricoStatusPedidoResponse]
)
def obter_historico_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        return pedido_service.obter_historico_status_pedido(db, pedido_id)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)


@router.get("/{pedido_id}/detalhado", response_model=PedidoDetalhadoResponse)
def obter_pedido_detalhado(pedido_id: int, db: Session = Depends(get_db)):
    """
    Retorna o pedido com seus itens e pagamento. Não inclui histórico de
    status (ver GET /pedidos/{pedido_id}/historico para isso).
    """
    try:
        return pedido_service.obter_pedido_detalhado(db, pedido_id)
    except EntidadeNaoEncontrada as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=erro.mensagem)
