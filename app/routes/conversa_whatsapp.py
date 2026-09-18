from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.conversa_whatsapp import ConversaWhatsappResponse
from app.services import conversa_whatsapp_service
from pydantic import BaseModel

class EstadoConversaUpdate(BaseModel):
    estado: str

router = APIRouter(
    prefix="/conversas-whatsapp",
    tags=["Conversas WhatsApp"],
)


@router.get(
    "/{telefone}",
    response_model=ConversaWhatsappResponse,
)
def obter_conversa(
    telefone: str,
    db: Session = Depends(get_db),
):
    conversa = conversa_whatsapp_service.obter_conversa_por_telefone(
        db,
        telefone,
    )

    if conversa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada.",
        )

    return conversa


@router.post(
    "",
    response_model=ConversaWhatsappResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_conversa(
    telefone: str,
    db: Session = Depends(get_db),
):
    conversa_existente = (
        conversa_whatsapp_service.obter_conversa_por_telefone(
            db,
            telefone,
        )
    )

    if conversa_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma conversa para este telefone.",
        )

    return conversa_whatsapp_service.criar_conversa(
        db,
        telefone,
    )


@router.patch(
    "/{telefone}/estado",
    response_model=ConversaWhatsappResponse,
)
def alterar_estado(
    telefone: str,
    dados: EstadoConversaUpdate,
    db: Session = Depends(get_db),
):
    conversa = conversa_whatsapp_service.obter_conversa_por_telefone(
        db,
        telefone,
    )

    if conversa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada.",
        )

    try:
        return conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
            dados.estado,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )