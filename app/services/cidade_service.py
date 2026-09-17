from sqlalchemy.orm import Session

from app.models.cidade import Cidade
from app.schemas.cidade import CidadeCreate, CidadeUpdate


def criar_cidade(db: Session, dados: CidadeCreate) -> Cidade:
    cidade = Cidade(**dados.model_dump())
    db.add(cidade)
    db.commit()
    db.refresh(cidade)
    return cidade


def listar_cidades(db: Session, skip: int = 0, limit: int = 100) -> list[Cidade]:
    return db.query(Cidade).offset(skip).limit(limit).all()


def obter_cidade(db: Session, cidade_id: int) -> Cidade | None:
    return db.get(Cidade, cidade_id)


def atualizar_cidade(db: Session, cidade_id: int, dados: CidadeUpdate) -> Cidade | None:
    cidade = obter_cidade(db, cidade_id)
    if cidade is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(cidade, campo, valor)
    db.commit()
    db.refresh(cidade)
    return cidade


def desativar_cidade(db: Session, cidade_id: int) -> Cidade | None:
    """Desativação lógica (soft delete) - nunca remove o registro fisicamente."""
    cidade = obter_cidade(db, cidade_id)
    if cidade is None:
        return None
    cidade.ativo = False
    db.commit()
    db.refresh(cidade)
    return cidade
