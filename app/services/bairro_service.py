from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bairro import Bairro
from app.models.cidade import Cidade
from app.schemas.bairro import BairroCreate, BairroUpdate
from app.services.exceptions import ConflitoDados, EntidadeNaoEncontrada, ErroNegocio


def _validar_cidade(db: Session, cidade_id: int) -> None:
    cidade = db.get(Cidade, cidade_id)
    if cidade is None:
        raise EntidadeNaoEncontrada("Cidade informada não existe.")
    if not cidade.ativo:
        raise ErroNegocio("Não é possível criar um bairro em uma cidade inativa.")


def _validar_nome(
    db: Session, nome: str, cidade_id: int, bairro_id: int | None = None
) -> str:
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ErroNegocio("Nome do bairro é obrigatório.")

    consulta = db.query(Bairro).filter(
        func.lower(Bairro.nome) == nome_limpo.lower(),
        Bairro.cidade_id == cidade_id,
        Bairro.ativo.is_(True),
    )
    if bairro_id is not None:
        consulta = consulta.filter(Bairro.id != bairro_id)
    if consulta.first() is not None:
        raise ConflitoDados("Já existe um bairro ativo com este nome nesta cidade.")

    return nome_limpo


def _validar_taxa(valor_taxa_entrega: Decimal) -> Decimal:
    if valor_taxa_entrega < 0:
        raise ErroNegocio("A taxa de entrega não pode ser negativa.")
    return valor_taxa_entrega


def criar_bairro(db: Session, dados: BairroCreate) -> Bairro:
    _validar_cidade(db, dados.cidade_id)
    nome = _validar_nome(db, dados.nome, dados.cidade_id)
    taxa = _validar_taxa(dados.valor_taxa_entrega)

    bairro = Bairro(cidade_id=dados.cidade_id, nome=nome, valor_taxa_entrega=taxa)
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

    valores = dados.model_dump(exclude_unset=True)
    cidade_id_alvo = valores.get("cidade_id", bairro.cidade_id)

    if "cidade_id" in valores:
        _validar_cidade(db, valores["cidade_id"])
    if "nome" in valores:
        valores["nome"] = _validar_nome(db, valores["nome"], cidade_id_alvo, bairro_id)
    if "valor_taxa_entrega" in valores:
        valores["valor_taxa_entrega"] = _validar_taxa(valores["valor_taxa_entrega"])

    for campo, valor in valores.items():
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
