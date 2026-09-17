from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


def criar_categoria(db: Session, dados: CategoriaCreate) -> Categoria:
    categoria = Categoria(**dados.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def listar_categorias(db: Session, skip: int = 0, limit: int = 100) -> list[Categoria]:
    return db.query(Categoria).offset(skip).limit(limit).all()


def obter_categoria(db: Session, categoria_id: int) -> Categoria | None:
    return db.get(Categoria, categoria_id)


def atualizar_categoria(
    db: Session, categoria_id: int, dados: CategoriaUpdate
) -> Categoria | None:
    categoria = obter_categoria(db, categoria_id)
    if categoria is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria


def desativar_categoria(db: Session, categoria_id: int) -> Categoria | None:
    """Desativação lógica (soft delete) - nunca remove o registro fisicamente."""
    categoria = obter_categoria(db, categoria_id)
    if categoria is None:
        return None
    categoria.ativo = False
    db.commit()
    db.refresh(categoria)
    return categoria
