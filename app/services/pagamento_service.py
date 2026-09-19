from datetime import datetime

from sqlalchemy.orm import Session

from app.models.pagamento import Pagamento
from app.models.enums import FormaPagamento, StatusPagamento
from app.models.cobranca_pix import CobrancaPix


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
    novo_status = dados.get("status_pagamento")
    nova_forma = dados.get("forma_pagamento")

    if novo_status is not None:
        if pagamento.status_pagamento != StatusPagamento.PENDENTE:
            raise ValueError(
                "Somente pagamentos pendentes podem ter o status alterado."
            )

        if novo_status not in (
            StatusPagamento.PAGO,
            StatusPagamento.CANCELADO,
        ):
            raise ValueError(
                "Transição de status de pagamento inválida."
            )

    if nova_forma is not None:
        if pagamento.status_pagamento != StatusPagamento.PENDENTE:
            raise ValueError(
                "A forma de pagamento só pode ser alterada enquanto "
                "o pagamento estiver pendente."
            )

        if nova_forma not in (
            FormaPagamento.DINHEIRO,
            FormaPagamento.PIX,
            FormaPagamento.CARTAO,
        ):
            raise ValueError("Forma de pagamento inválida.")

    if novo_status == StatusPagamento.PAGO:
        dados["data_pagamento"] = datetime.now()

    dados.pop("pedido_id", None)
    dados.pop("valor", None)

    for campo, valor in dados.items():
        setattr(pagamento, campo, valor)

    db.commit()
    db.refresh(pagamento)

    return pagamento

def criar_cobranca_pix(
    db: Session,
    pagamento: Pagamento,
    asaas_payment_id: str,
    pix_payload: str,
    pix_expira_em: datetime,
    status_externo: str,
) -> CobrancaPix:
    cobranca = CobrancaPix(
        pagamento_id=pagamento.id,
        asaas_payment_id=asaas_payment_id,
        pix_payload=pix_payload,
        pix_expira_em=pix_expira_em,
        status_externo=status_externo,
    )

    db.add(cobranca)
    db.commit()
    db.refresh(cobranca)

    return cobranca