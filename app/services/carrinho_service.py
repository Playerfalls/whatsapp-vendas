from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.carrinho import Carrinho
from app.models.conversa_whatsapp import ConversaWhatsapp
from app.models.item_carrinho import ItemCarrinho
from app.models.produto import Produto


def obter_ou_criar_carrinho(
    db: Session,
    conversa: ConversaWhatsapp,
) -> Carrinho:
    carrinho = (
        db.query(Carrinho)
        .filter(Carrinho.conversa_id == conversa.id)
        .first()
    )

    if carrinho is not None:
        return carrinho

    carrinho = Carrinho(
        conversa_id=conversa.id,
    )

    db.add(carrinho)
    db.commit()
    db.refresh(carrinho)

    return carrinho


def adicionar_item(
    db: Session,
    carrinho: Carrinho,
    produto: Produto,
    quantidade: int,
) -> ItemCarrinho:
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    if not produto.ativo:
        raise ValueError("O produto não está disponível.")

    item = (
        db.query(ItemCarrinho)
        .filter(
            ItemCarrinho.carrinho_id == carrinho.id,
            ItemCarrinho.produto_id == produto.id,
        )
        .first()
    )

    if item is not None:
        nova_quantidade = item.quantidade + quantidade

        if nova_quantidade > produto.quantidade_estoque:
            raise ValueError(
                "Quantidade solicitada maior que o estoque disponível."
            )

        item.quantidade = nova_quantidade

    else:
        if quantidade > produto.quantidade_estoque:
            raise ValueError(
                "Quantidade solicitada maior que o estoque disponível."
            )

        item = ItemCarrinho(
            carrinho_id=carrinho.id,
            produto_id=produto.id,
            quantidade=quantidade,
            preco_unitario=produto.preco,
        )
        db.add(item)

    db.commit()
    db.refresh(item)

    return item

def listar_itens(
    db: Session,
    carrinho: Carrinho,
) -> list[ItemCarrinho]:
    return (
        db.query(ItemCarrinho)
        .filter(ItemCarrinho.carrinho_id == carrinho.id)
        .all()
    )


def calcular_total(
    db: Session,
    carrinho: Carrinho,
) -> Decimal:
    itens = listar_itens(db, carrinho)

    return sum(
        (
            item.preco_unitario * item.quantidade
            for item in itens
        ),
        Decimal("0.00"),
    )


def remover_item(
    db: Session,
    carrinho: Carrinho,
    produto_id: int,
) -> bool:
    item = (
        db.query(ItemCarrinho)
        .filter(
            ItemCarrinho.carrinho_id == carrinho.id,
            ItemCarrinho.produto_id == produto_id,
        )
        .first()
    )

    if item is None:
        return False

    db.delete(item)
    db.commit()

    return True


def alterar_quantidade(
    db: Session,
    carrinho: Carrinho,
    produto_id: int,
    quantidade: int,
) -> ItemCarrinho | None:
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    item = (
        db.query(ItemCarrinho)
        .filter(
            ItemCarrinho.carrinho_id == carrinho.id,
            ItemCarrinho.produto_id == produto_id,
        )
        .first()
    )

    if item is None:
        return None

    produto = db.get(Produto, produto_id)

    if produto is None:
        raise ValueError("Produto não encontrado.")

    if not produto.ativo:
        raise ValueError("O produto não está disponível.")

    if quantidade > produto.quantidade_estoque:
        raise ValueError(
            "Quantidade solicitada maior que o estoque disponível."
        )

    item.quantidade = quantidade

    db.commit()
    db.refresh(item)

    return item
def limpar_carrinho(
    db: Session,
    carrinho: Carrinho,
) -> None:
    itens = listar_itens(db, carrinho)

    for item in itens:
        db.delete(item)

    db.commit()


def formatar_resumo(
    db: Session,
    carrinho: Carrinho,
) -> str:
    itens = listar_itens(db, carrinho)

    if not itens:
        return "Seu carrinho está vazio."

    linhas = ["🛒 Resumo do seu pedido:\n"]

    for item in itens:
        subtotal = item.preco_unitario * item.quantidade

        linhas.append(
            f"{item.quantidade}x {item.produto.nome} "
            f"— R$ {subtotal:.2f}"
        )

    total = calcular_total(db, carrinho)

    linhas.append(f"\n💰 Total: R$ {total:.2f}")

    return "\n".join(linhas)