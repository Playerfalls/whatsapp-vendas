from sqlalchemy.orm import Session

from app.models.endereco import Endereco
from app.schemas.endereco import EnderecoCreate, EnderecoUpdate


def criar_endereco(db: Session, dados: EnderecoCreate) -> Endereco:
    endereco = Endereco(**dados.model_dump())
    db.add(endereco)
    db.commit()
    db.refresh(endereco)
    return endereco


def listar_enderecos(db: Session, skip: int = 0, limit: int = 100) -> list[Endereco]:
    return db.query(Endereco).offset(skip).limit(limit).all()


def obter_endereco(db: Session, endereco_id: int) -> Endereco | None:
    return db.get(Endereco, endereco_id)


def atualizar_endereco(
    db: Session, endereco_id: int, dados: EnderecoUpdate
) -> Endereco | None:
    endereco = obter_endereco(db, endereco_id)
    if endereco is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(endereco, campo, valor)
    db.commit()
    db.refresh(endereco)
    return endereco


def desativar_endereco(db: Session, endereco_id: int) -> Endereco | None:
    """Desativação lógica (soft delete) - nunca remove o registro fisicamente."""
    endereco = obter_endereco(db, endereco_id)
    if endereco is None:
        return None
    endereco.ativo = False
    db.commit()
    db.refresh(endereco)
    return endereco
