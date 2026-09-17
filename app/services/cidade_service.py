from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.cidade import Cidade
from app.schemas.cidade import CidadeCreate, CidadeUpdate
from app.services.exceptions import ConflitoDados, ErroNegocio


def _validar_nome(db: Session, nome: str, cidade_id: int | None = None) -> str:
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ErroNegocio("Nome da cidade é obrigatório.")

    consulta = db.query(Cidade).filter(
        func.lower(Cidade.nome) == nome_limpo.lower(), Cidade.ativo.is_(True)
    )
    if cidade_id is not None:
        consulta = consulta.filter(Cidade.id != cidade_id)
    if consulta.first() is not None:
        raise ConflitoDados("Já existe uma cidade ativa com este nome.")

    return nome_limpo


def criar_cidade(db: Session, dados: CidadeCreate) -> Cidade:
    nome = _validar_nome(db, dados.nome)
    cidade = Cidade(nome=nome)
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

    valores = dados.model_dump(exclude_unset=True)
    if "nome" in valores:
        valores["nome"] = _validar_nome(db, valores["nome"], cidade_id)

    for campo, valor in valores.items():
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
