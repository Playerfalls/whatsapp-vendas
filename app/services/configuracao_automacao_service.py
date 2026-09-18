from sqlalchemy.orm import Session

from app.models.configuracao_automacao import ConfiguracaoAutomacao


def obter_configuracao(db: Session) -> ConfiguracaoAutomacao:
    configuracao = db.query(ConfiguracaoAutomacao).first()

    if configuracao is None:
        configuracao = ConfiguracaoAutomacao(ativa=True)
        db.add(configuracao)
        db.commit()
        db.refresh(configuracao)

    return configuracao


def atualizar_automacao(
    db: Session,
    ativa: bool,
) -> ConfiguracaoAutomacao:
    configuracao = obter_configuracao(db)

    configuracao.ativa = ativa

    db.commit()
    db.refresh(configuracao)

    return configuracao