import unicodedata

from decimal import Decimal

from sqlalchemy.orm import Session
from difflib import SequenceMatcher

from app.models.categoria import Categoria
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.services.exceptions import EntidadeNaoEncontrada, ErroNegocio


def _validar_nome(nome: str) -> str:
    nome_limpo = nome.strip()
    if not nome_limpo:
        raise ErroNegocio("Nome do produto é obrigatório.")
    return nome_limpo


def _validar_preco(preco: Decimal) -> Decimal:
    if preco < 0:
        raise ErroNegocio("O preço do produto não pode ser negativo.")
    return preco


def _validar_estoque(quantidade_estoque: int) -> int:
    if quantidade_estoque < 0:
        raise ErroNegocio("A quantidade em estoque não pode ser negativa.")
    return quantidade_estoque


def _validar_categoria(db: Session, categoria_id: int) -> None:
    categoria = db.get(Categoria, categoria_id)
    if categoria is None:
        raise EntidadeNaoEncontrada("Categoria informada não existe.")
    if not categoria.ativo:
        raise ErroNegocio("Não é possível usar uma categoria inativa para o produto.")


def criar_produto(db: Session, dados: ProdutoCreate) -> Produto:
    _validar_categoria(db, dados.categoria_id)
    nome = _validar_nome(dados.nome)
    preco = _validar_preco(dados.preco)
    quantidade_estoque = _validar_estoque(dados.quantidade_estoque)

    produto = Produto(
        categoria_id=dados.categoria_id,
        nome=nome,
        descricao=dados.descricao,
        preco=preco,
        quantidade_estoque=quantidade_estoque,
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def listar_produtos(db: Session, skip: int = 0, limit: int = 100) -> list[Produto]:
    return db.query(Produto).offset(skip).limit(limit).all()

def listar_catalogo(
    db: Session,
) -> list[Produto]:
    return (
        db.query(Produto)
        .filter(Produto.ativo.is_(True))
        .order_by(Produto.categoria_id, Produto.nome)
        .all()
    )

def formatar_catalogo(
    produtos: list[Produto],
) -> str:
    if not produtos:
        return "No momento, não há produtos disponíveis."

    categorias = {}

    for produto in produtos:
        categorias.setdefault(produto.categoria_id, []).append(produto)

    linhas = [
        "🛒 *Nosso catálogo*",
        "",
    ]

    for produtos_categoria in categorias.values():
        categoria = produtos_categoria[0].categoria

        linhas.append(f"📦 *{categoria.nome}*")

        for produto in produtos_categoria:
            preco = f"{produto.preco:.2f}".replace(".", ",")

            linhas.append(
                f"• {produto.nome} — R$ {preco}"
            )

        linhas.append("")

    linhas.append("Digite os produtos que deseja.")

    return "\n".join(linhas)

def obter_produto(db: Session, produto_id: int) -> Produto | None:
    return db.get(Produto, produto_id)


def atualizar_produto(
    db: Session, produto_id: int, dados: ProdutoUpdate
) -> Produto | None:
    produto = obter_produto(db, produto_id)
    if produto is None:
        return None

    valores = dados.model_dump(exclude_unset=True)
    if "categoria_id" in valores:
        _validar_categoria(db, valores["categoria_id"])
    if "nome" in valores:
        valores["nome"] = _validar_nome(valores["nome"])
    if "preco" in valores:
        valores["preco"] = _validar_preco(valores["preco"])
    if "quantidade_estoque" in valores:
        valores["quantidade_estoque"] = _validar_estoque(valores["quantidade_estoque"])

    for campo, valor in valores.items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto


def desativar_produto(db: Session, produto_id: int) -> Produto | None:
    """
    Desativação lógica (soft delete) - nunca remove o registro fisicamente.
    Não mexe em `quantidade_estoque`: baixa de estoque é regra de fase futura.
    """
    produto = obter_produto(db, produto_id)
    if produto is None:
        return None
    produto.ativo = False
    db.commit()
    db.refresh(produto)
    return produto

def _normalizar_texto(texto: str) -> str:
    texto_normalizado = texto.strip().lower()
    texto_normalizado = unicodedata.normalize(
        "NFD",
        texto_normalizado,
    )

    texto_normalizado = "".join(
        caractere
        for caractere in texto_normalizado
        if unicodedata.category(caractere) != "Mn"
    )

    return _normalizar_plural(texto_normalizado)


def _normalizar_plural(texto: str) -> str:
    palavras = texto.split()

    palavras_normalizadas = []

    for palavra in palavras:
        if palavra.endswith("oes") and len(palavra) > 4:
            palavra = palavra[:-3] + "ao"
        elif palavra.endswith("s") and len(palavra) > 3:
            palavra = palavra[:-1]

        palavras_normalizadas.append(palavra)

    return " ".join(palavras_normalizadas)

def buscar_produtos_por_nome(
    db: Session,
    texto: str,
) -> list[Produto]:
    texto_normalizado = _normalizar_texto(texto)

    if not texto_normalizado:
        return []

    return (
        db.query(Produto)
        .filter(
            Produto.ativo.is_(True),
            Produto.nome.ilike(f"%{texto_normalizado}%"),
        )
        .all()
    )
def _calcular_similaridade(texto_a: str, texto_b: str) -> float:
    return SequenceMatcher(
        None,
        _normalizar_texto(texto_a),
        _normalizar_texto(texto_b),
    ).ratio()

def buscar_produtos_por_similaridade(
    db: Session,
    texto: str,
    limite: float = 0.85,
) -> list[Produto]:
    texto_normalizado = _normalizar_texto(texto)

    if not texto_normalizado:
        return []

    produtos = (
        db.query(Produto)
        .filter(Produto.ativo.is_(True))
        .all()
    )

    candidatos = []

    for produto in produtos:
        nome_normalizado = _normalizar_texto(produto.nome)

        if texto_normalizado in nome_normalizado:
            candidatos.append(produto)
            continue

        palavras_nome = nome_normalizado.split()

        for palavra in palavras_nome:
            similaridade = _calcular_similaridade(
                texto_normalizado,
                palavra,
            )

            if similaridade >= limite:
                candidatos.append(produto)
                break

    return candidatos

def identificar_produto(
    db: Session,
    texto: str,
) -> Produto | list[Produto] | None:
    candidatos = buscar_produtos_por_similaridade(
        db,
        texto,
    )

    if not candidatos:
        return None

    if len(candidatos) == 1:
        return candidatos[0]

    return candidatos

def interpretar_produto(
    db: Session,
    texto: str,
) -> dict:
    resultado = identificar_produto(
        db,
        texto,
    )

    if resultado is None:
        return {
            "status": "NAO_ENCONTRADO",
            "produto": None,
            "candidatos": [],
            "mensagem": (
                "Não consegui identificar esse produto. 🤔 "
                "Pode verificar se a digitação está correta "
                "e enviar novamente?"
            ),
        }

    if isinstance(resultado, Produto):
        return {
            "status": "IDENTIFICADO",
            "produto": resultado,
            "candidatos": [],
            "mensagem": "Produto identificado.",
        }

    return {
        "status": "AMBIGUO",
        "produto": None,
        "candidatos": resultado,
        "mensagem": (
            "Encontrei mais de uma opção para esse produto. "
            "Qual delas você deseja?"
        ),
    }

def extrair_quantidade(texto: str) -> tuple[int | None, str]:
    texto_limpo = texto.strip()

    partes = texto_limpo.split(maxsplit=1)

    if not partes:
        return 1, ""

    primeira_parte = partes[0]

    if primeira_parte.isdigit():
        quantidade = int(primeira_parte)

        if len(partes) == 1:
            return quantidade if quantidade > 0 else None, ""

        return (
            quantidade if quantidade > 0 else None,
            partes[1],
        )

    return 1, texto_limpo

def extrair_quantidade(texto: str) -> tuple[int | None, str]:
    texto_limpo = texto.strip()

    partes = texto_limpo.split(maxsplit=1)

    if not partes:
        return 1, ""

    primeira_parte = partes[0]

    if primeira_parte.lstrip("-").isdigit():
        quantidade = int(primeira_parte)

        if len(partes) == 1:
            return quantidade if quantidade > 0 else None, ""

        return (
            quantidade if quantidade > 0 else None,
            partes[1],
        )

    return 1, texto_limpo