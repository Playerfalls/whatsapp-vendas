from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.pagamento import Pagamento
from app.schemas.pagamento import (
    PagamentoCreate,
    PagamentoResponse,
    PagamentoUpdate,
)
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


@router.post(
    "",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_pagamento(
    dados: PagamentoCreate,
    db: Session = Depends(get_db),
):
    pagamento = Pagamento(**dados.model_dump())

    return pagamento_service.criar_pagamento(db, pagamento)


@router.patch(
    "/{pagamento_id}",
    response_model=PagamentoResponse,
)
def atualizar_pagamento(
    pagamento_id: int,
    dados: PagamentoUpdate,
    db: Session = Depends(get_db),
):
    pagamento = db.query(Pagamento).filter(
        Pagamento.id == pagamento_id
    ).first()

    if pagamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado.",
        )

    dados_atualizacao = dados.model_dump(
        exclude_unset=True,
        exclude={"pedido_id"},
    )

    return pagamento_service.atualizar_pagamento(
        db,
        pagamento,
        dados_atualizacao,
    )