from sqlalchemy.orm import Session

from app.models.bairro import Bairro
from app.models.cliente import Cliente
from app.models.endereco import Endereco
from app.schemas.endereco import EnderecoCreate, EnderecoUpdate
from app.services.exceptions import EntidadeNaoEncontrada, ErroNegocio


def _validar_cliente(db: Session, cliente_id: int) -> None:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise EntidadeNaoEncontrada("Cliente informado não existe.")
    if not cliente.ativo:
        raise ErroNegocio("Não é possível usar um cliente inativo para o endereço.")


def _validar_bairro(db: Session, bairro_id: int) -> None:
    bairro = db.get(Bairro, bairro_id)
    if bairro is None:
        raise EntidadeNaoEncontrada("Bairro informado não existe.")
    if not bairro.ativo:
        raise ErroNegocio("Não é possível usar um bairro inativo para o endereço.")


def _validar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
    valor_limpo = valor.strip()
    if not valor_limpo:
        raise ErroNegocio(f"{nome_campo} é obrigatório.")
    return valor_limpo


def criar_endereco(db: Session, dados: EnderecoCreate) -> Endereco:
    _validar_cliente(db, dados.cliente_id)
    _validar_bairro(db, dados.bairro_id)

    valores = dados.model_dump()
    valores["cep"] = _validar_texto_obrigatorio(valores["cep"], "CEP")
    valores["logradouro"] = _validar_texto_obrigatorio(
        valores["logradouro"], "Logradouro"
    )
    valores["numero"] = _validar_texto_obrigatorio(valores["numero"], "Número")

    endereco = Endereco(**valores)
    db.add(endereco)
    db.commit()
    db.refresh(endereco)
    return endereco


def listar_enderecos(db: Session, skip: int = 0, limit: int = 100) -> list[Endereco]:
    return db.query(Endereco).offset(skip).limit(limit).all()

def listar_enderecos_do_cliente(
    db: Session,
    cliente_id: int,
) -> list[Endereco]:
    return (
        db.query(Endereco)
        .filter(
            Endereco.cliente_id == cliente_id,
            Endereco.ativo.is_(True),
        )
        .all()
    )

def obter_endereco(db: Session, endereco_id: int) -> Endereco | None:
    return db.get(Endereco, endereco_id)


def atualizar_endereco(
    db: Session, endereco_id: int, dados: EnderecoUpdate
) -> Endereco | None:
    endereco = obter_endereco(db, endereco_id)
    if endereco is None:
        return None

    valores = dados.model_dump(exclude_unset=True)
    if "cliente_id" in valores:
        _validar_cliente(db, valores["cliente_id"])
    if "bairro_id" in valores:
        _validar_bairro(db, valores["bairro_id"])
    if "cep" in valores:
        valores["cep"] = _validar_texto_obrigatorio(valores["cep"], "CEP")
    if "logradouro" in valores:
        valores["logradouro"] = _validar_texto_obrigatorio(
            valores["logradouro"], "Logradouro"
        )
    if "numero" in valores:
        valores["numero"] = _validar_texto_obrigatorio(valores["numero"], "Número")

    for campo, valor in valores.items():
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
