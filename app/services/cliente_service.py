from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.services.exceptions import ConflitoDados, ErroNegocio


def _normalizar_telefone(telefone: str) -> str:
    """Mantém apenas dígitos, removendo espaços e demais caracteres."""
    return "".join(caractere for caractere in telefone if caractere.isdigit())


def _validar_telefone(db: Session, telefone: str, cliente_id: int | None = None) -> str:
    telefone_normalizado = _normalizar_telefone(telefone)
    if not telefone_normalizado:
        raise ErroNegocio("Telefone é obrigatório.")

    consulta = db.query(Cliente).filter(
        Cliente.telefone == telefone_normalizado, Cliente.ativo.is_(True)
    )
    if cliente_id is not None:
        consulta = consulta.filter(Cliente.id != cliente_id)
    if consulta.first() is not None:
        raise ConflitoDados("Já existe um cliente ativo com este telefone.")

    return telefone_normalizado


def _validar_nome(nome: str) -> str:
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ErroNegocio("Nome é obrigatório.")
    return nome_limpo


def criar_cliente(db: Session, dados: ClienteCreate) -> Cliente:
    telefone = _validar_telefone(db, dados.telefone)
    nome = _validar_nome(dados.nome)

    cliente = Cliente(nome=nome, telefone=telefone)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def listar_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    return db.query(Cliente).offset(skip).limit(limit).all()


def obter_cliente(db: Session, cliente_id: int) -> Cliente | None:
    return db.get(Cliente, cliente_id)

def obter_cliente_por_telefone(
    db: Session,
    telefone: str,
) -> Cliente | None:
    telefone_normalizado = _normalizar_telefone(telefone)

    if not telefone_normalizado:
        return None

    return (
        db.query(Cliente)
        .filter(
            Cliente.telefone == telefone_normalizado,
            Cliente.ativo.is_(True),
        )
        .first()
    )

def atualizar_cliente(
    db: Session, cliente_id: int, dados: ClienteUpdate
) -> Cliente | None:
    cliente = obter_cliente(db, cliente_id)
    if cliente is None:
        return None

    valores = dados.model_dump(exclude_unset=True)
    if "telefone" in valores:
        valores["telefone"] = _validar_telefone(db, valores["telefone"], cliente_id)
    if "nome" in valores:
        valores["nome"] = _validar_nome(valores["nome"])

    for campo, valor in valores.items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


def desativar_cliente(db: Session, cliente_id: int) -> Cliente | None:
    """Desativação lógica (soft delete) - nunca remove o registro fisicamente."""
    cliente = obter_cliente(db, cliente_id)
    if cliente is None:
        return None
    cliente.ativo = False
    db.commit()
    db.refresh(cliente)
    return cliente
