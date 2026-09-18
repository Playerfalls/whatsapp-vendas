from sqlalchemy.orm import Session

from app.models.pagamento import Pagamento


def obter_pagamento_por_pedido(
    db: Session, pedido_id: int
) -> Pagamento | None:
    return (
        db.query(Pagamento)
        .filter(Pagamento.pedido_id == pedido_id)
        .first()
    )