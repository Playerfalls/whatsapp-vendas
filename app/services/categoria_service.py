from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from app.services.exceptions import ConflitoDados, ErroNegocio


def _validar_nome(db: Session, nome: str, categoria_id: int | None = None) -> str:
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ErroNegocio("Nome da categoria é obrigatório.")

    consulta = db.query(Categoria).filter(
        func.lower(Categoria.nome) == nome_limpo.lower(), Categoria.ativo.is_(True)
    )
    if categoria_id is not None:
        consulta = consulta.filter(Categoria.id != categoria_id)
    if consulta.first() is not None:
        raise ConflitoDados("Já existe uma categoria ativa com este nome.")

    return nome_limpo


def criar_categoria(db: Session, dados: CategoriaCreate) -> Categoria:
    nome = _validar_nome(db, dados.nome)
    categoria = Categoria(nome=nome)
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

    valores = dados.model_dump(exclude_unset=True)
    if "nome" in valores:
        valores["nome"] = _validar_nome(db, valores["nome"], categoria_id)

    for campo, valor in valores.items():
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
