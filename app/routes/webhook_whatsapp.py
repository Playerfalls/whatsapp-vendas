from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import whatsapp_service
from app.services import conversa_whatsapp_processador


router = APIRouter(
    prefix="/webhook/whatsapp",
    tags=["Webhook WhatsApp"],
)


@router.get("")
def verificar_webhook():
    return {
        "status": "ok",
        "mensagem": "Webhook WhatsApp ativo.",
    }


@router.post("")
def receber_webhook(
    dados: dict,
    db: Session = Depends(get_db),
):
    telefone = dados.get("telefone")

    if not telefone:
        return {
            "status": "erro",
            "mensagem": "Telefone não informado.",
        }

    if not whatsapp_service.automacao_esta_ativa(db):
        return {
            "status": "ignorado",
            "mensagem": "A automação está desativada.",
        }

    conversa = whatsapp_service.obter_ou_criar_conversa(
        db,
        telefone,
    )

    resposta = conversa_whatsapp_processador.processar_conversa(
        db,
        conversa,
        dados.get("mensagem", ""),
    )

    return {
        "status": "recebido",
        "conversa_id": conversa.id,
        "telefone": conversa.telefone,
        "estado": conversa.estado,
        "resposta": resposta,
    }
    