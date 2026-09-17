from sqlalchemy.orm import Session

from app.models.bairro import Bairro
from app.schemas.bairro import BairroCreate, BairroUpdate


def criar_bairro(db: Session, dados: BairroCreate) -> Bairro:
    bairro = Bairro(**dados.model_dump())
    db.add(bairro)
    db.commit()
    db.refresh(bairro)
    return bairro


def listar_bairros(db: Session, skip: int = 0, limit: int = 100) -> list[Bairro]:
    return db.query(Bairro).offset(skip).limit(limit).all()


def obter_bairro(db: Session, bairro_id: int) -> Bairro | None:
    return db.get(Bairro, bairro_id)


def atualizar_bairro(db: Session, bairro_id: int, dados: BairroUpdate) -> Bairro | None:
    bairro = obter_bairro(db, bairro_id)
    if bairro is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(bairro, campo, valor)
    db.commit()
    db.refresh(bairro)
    return bairro


def desativar_bairro(db: Session, bairro_id: int) -> Bairro | None:
    """Desativação lógica (soft delete) - nunca remove o registro fisicamente."""
    bairro = obter_bairro(db, bairro_id)
    if bairro is None:
        return None
    bairro.ativo = False
    db.commit()
    db.refresh(bairro)
    return bairro
