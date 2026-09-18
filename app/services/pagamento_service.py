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

def criar_pagamento(db: Session, pagamento: Pagamento) -> Pagamento:
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)

    return pagamento

def atualizar_pagamento(
    db: Session, pagamento: Pagamento, dados: dict
) -> Pagamento:
    for campo, valor in dados.items():
        setattr(pagamento, campo, valor)

    db.commit()
    db.refresh(pagamento)

    return pagamento