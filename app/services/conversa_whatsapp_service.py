from sqlalchemy.orm import Session

from app.models.conversa_whatsapp import ConversaWhatsapp
from app.services.conversa_whatsapp_estado import TRANSICOES_PERMITIDAS


def obter_conversa_por_telefone(
    db: Session,
    telefone: str,
) -> ConversaWhatsapp | None:
    return (
        db.query(ConversaWhatsapp)
        .filter(ConversaWhatsapp.telefone == telefone)
        .first()
    )


def criar_conversa(
    db: Session,
    telefone: str,
) -> ConversaWhatsapp:
    conversa = ConversaWhatsapp(
        telefone=telefone,
        estado="INICIO",
    )

    db.add(conversa)
    db.commit()
    db.refresh(conversa)

    return conversa


def atualizar_conversa(
    db: Session,
    conversa: ConversaWhatsapp,
    dados: dict,
) -> ConversaWhatsapp:
    for campo, valor in dados.items():
        setattr(conversa, campo, valor)

    db.commit()
    db.refresh(conversa)

    return conversa


def alterar_estado(
    db: Session,
    conversa: ConversaWhatsapp,
    novo_estado: str,
) -> ConversaWhatsapp:
    estados_permitidos = TRANSICOES_PERMITIDAS.get(
        conversa.estado,
        set(),
    )

    if novo_estado not in estados_permitidos:
        raise ValueError(
            f"Não é permitido alterar a conversa de "
            f"{conversa.estado} para {novo_estado}."
        )

    conversa.estado = novo_estado

    db.commit()
    db.refresh(conversa)

    return conversa