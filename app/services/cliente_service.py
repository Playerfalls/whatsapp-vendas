from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def criar_cliente(db: Session, dados: ClienteCreate) -> Cliente:
    cliente = Cliente(**dados.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def listar_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    return db.query(Cliente).offset(skip).limit(limit).all()


def obter_cliente(db: Session, cliente_id: int) -> Cliente | None:
    return db.get(Cliente, cliente_id)


def atualizar_cliente(
    db: Session, cliente_id: int, dados: ClienteUpdate
) -> Cliente | None:
    cliente = obter_cliente(db, cliente_id)
    if cliente is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
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
