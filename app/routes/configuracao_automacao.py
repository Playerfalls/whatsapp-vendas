from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.configuracao_automacao import (
    ConfiguracaoAutomacaoResponse,
    ConfiguracaoAutomacaoUpdate,
)
from app.services import configuracao_automacao_service


router = APIRouter(
    prefix="/configuracao-automacao",
    tags=["Configuração da Automação"],
)


@router.get("", response_model=ConfiguracaoAutomacaoResponse)
def obter_configuracao(db: Session = Depends(get_db)):
    return configuracao_automacao_service.obter_configuracao(db)


@router.patch("", response_model=ConfiguracaoAutomacaoResponse)
def atualizar_automacao(
    dados: ConfiguracaoAutomacaoUpdate,
    db: Session = Depends(get_db),
):
    return configuracao_automacao_service.atualizar_automacao(
        db,
        dados.ativa,
    )