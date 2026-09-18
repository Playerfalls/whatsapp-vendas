from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.pagamento import PagamentoResponse
from app.services import pagamento_service

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.get(
    "/pedido/{pedido_id}",
    response_model=PagamentoResponse,
)
def obter_pagamento_por_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
):
    pagamento = pagamento_service.obter_pagamento_por_pedido(db, pedido_id)

    if pagamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado.",
        )

    return pagamento