from sqlalchemy.orm import Session

from app.models.conversa_whatsapp import ConversaWhatsapp
from app.services import conversa_whatsapp_service
from app.services import configuracao_automacao_service


def obter_ou_criar_conversa(
    db: Session,
    telefone: str,
) -> ConversaWhatsapp:
    conversa = (
        conversa_whatsapp_service.obter_conversa_por_telefone(
            db,
            telefone,
        )
    )

    if conversa is not None:
        return conversa

    return conversa_whatsapp_service.criar_conversa(
        db,
        telefone,
    )

def automacao_esta_ativa(db: Session) -> bool:
    configuracao = configuracao_automacao_service.obter_configuracao(db)
    return configuracao.ativa