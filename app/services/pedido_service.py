from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.models.endereco import Endereco
from app.models.enums import StatusPagamento, StatusPedido
from app.models.historico_status_pedido import HistoricoStatusPedido
from app.models.item_pedido import ItemPedido
from app.models.pagamento import Pagamento
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.schemas.pedido import PedidoCreate
from app.services.exceptions import EntidadeNaoEncontrada, ErroNegocio


def _validar_cliente(db: Session, cliente_id: int) -> Cliente:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise EntidadeNaoEncontrada("Cliente informado não existe.")
    if not cliente.ativo:
        raise ErroNegocio("Não é possível criar um pedido para um cliente inativo.")
    return cliente


def _validar_endereco(db: Session, endereco_id: int, cliente_id: int) -> Endereco:
    endereco = db.get(Endereco, endereco_id)
    if endereco is None:
        raise EntidadeNaoEncontrada("Endereço informado não existe.")
    if not endereco.ativo:
        raise ErroNegocio("Não é possível criar um pedido com um endereço inativo.")
    if endereco.cliente_id != cliente_id:
        raise ErroNegocio("O endereço informado não pertence ao cliente informado.")
    return endereco


def _validar_lista_itens(itens_dados: list) -> None:
    if not itens_dados:
        raise ErroNegocio("O pedido precisa ter pelo menos um item.")
    for item_dados in itens_dados:
        if item_dados.quantidade <= 0:
            raise ErroNegocio("A quantidade de cada item deve ser maior que zero.")


def _validar_produto(db: Session, produto_id: int, quantidade: int) -> Produto:
    produto = db.get(Produto, produto_id)
    if produto is None:
        raise EntidadeNaoEncontrada(f"Produto informado (id={produto_id}) não existe.")
    if not produto.ativo:
        raise ErroNegocio(f"O produto '{produto.nome}' está inativo.")
    if produto.quantidade_estoque < quantidade:
        raise ErroNegocio(
            f"Estoque insuficiente para o produto '{produto.nome}'. "
            f"Disponível: {produto.quantidade_estoque}, solicitado: {quantidade}."
        )
    return produto


def criar_pedido(db: Session, dados: PedidoCreate) -> Pedido:
    """
    Cria um pedido completo (Pedido + ItemPedido + Pagamento +
    HistoricoStatusPedido) em uma única transação.

    Nunca confia em preço, subtotal, taxa de entrega ou valor total
    vindos da entrada (`dados`) — todos esses valores são buscados/
    calculados aqui a partir do estado atual de Produto e Bairro.
    """
    cliente = _validar_cliente(db, dados.cliente_id)
    endereco = _validar_endereco(db, dados.endereco_id, dados.cliente_id)
    _validar_lista_itens(dados.itens)

    bairro = endereco.bairro
    cidade = bairro.cidade

    itens_pedido: list[ItemPedido] = []
    valor_itens = Decimal("0")

    for item_dados in dados.itens:
        produto = _validar_produto(db, item_dados.produto_id, item_dados.quantidade)
        preco_unitario = produto.preco
        subtotal = preco_unitario * item_dados.quantidade
        valor_itens += subtotal

        itens_pedido.append(
            ItemPedido(
                produto_id=produto.id,
                quantidade=item_dados.quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal,
            )
        )

    taxa_entrega_aplicada = bairro.valor_taxa_entrega
    valor_total = valor_itens + taxa_entrega_aplicada

    pedido = Pedido(
        cliente_id=cliente.id,
        endereco_id=endereco.id,
        cep_entrega=endereco.cep,
        logradouro_entrega=endereco.logradouro,
        numero_entrega=endereco.numero,
        complemento_entrega=endereco.complemento,
        ponto_referencia_entrega=endereco.ponto_referencia,
        bairro_entrega_nome=bairro.nome,
        cidade_entrega_nome=cidade.nome,
        taxa_entrega_aplicada=taxa_entrega_aplicada,
        status=StatusPedido.NOVO,
        valor_total=valor_total,
    )
    pedido.itens = itens_pedido
    pedido.pagamento = Pagamento(
        forma_pagamento=dados.forma_pagamento,
        status_pagamento=StatusPagamento.PENDENTE,
        valor=valor_total,
    )
    pedido.historico_status = [
        HistoricoStatusPedido(status_anterior=None, status_novo=StatusPedido.NOVO)
    ]

    db.add(pedido)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(pedido)
    return pedido


def listar_pedidos(db: Session, skip: int = 0, limit: int = 100) -> list[Pedido]:
    return db.query(Pedido).offset(skip).limit(limit).all()


def obter_pedido(db: Session, pedido_id: int) -> Pedido | None:
    return db.get(Pedido, pedido_id)


def atualizar_status_pedido(
    db: Session, pedido_id: int, novo_status: StatusPedido
) -> Pedido:
    """
    Altera o status de um pedido e registra a mudança em
    HistoricoStatusPedido, na mesma transação.
    """
    pedido = db.get(Pedido, pedido_id)
    if pedido is None:
        raise EntidadeNaoEncontrada("Pedido não encontrado.")

    status_anterior = pedido.status
    pedido.status = novo_status

    db.add(
        HistoricoStatusPedido(
            pedido_id=pedido.id,
            status_anterior=status_anterior,
            status_novo=novo_status,
        )
    )

    db.commit()
    db.refresh(pedido)
    return pedido


def obter_historico_status_pedido(
    db: Session, pedido_id: int
) -> list[HistoricoStatusPedido]:
    """Retorna o histórico de status de um pedido, em ordem cronológica."""
    pedido = db.get(Pedido, pedido_id)
    if pedido is None:
        raise EntidadeNaoEncontrada("Pedido não encontrado.")

    return (
        db.query(HistoricoStatusPedido)
        .filter(HistoricoStatusPedido.pedido_id == pedido_id)
        .order_by(HistoricoStatusPedido.id)
        .all()
    )


def obter_pedido_detalhado(db: Session, pedido_id: int) -> Pedido:
    """
    Busca um pedido para exibição detalhada (com itens e pagamento).
    Nenhum valor é recalculado aqui - a agregação/renomeação de campos
    para a resposta é feita inteiramente por PedidoDetalhadoResponse.
    """
    pedido = db.get(Pedido, pedido_id)
    if pedido is None:
        raise EntidadeNaoEncontrada("Pedido não encontrado.")
    return pedido


def cancelar_pedido(db: Session, pedido_id: int) -> Pedido:
    """
    Cancela um pedido (status -> CANCELADO), registrando a mudança em
    HistoricoStatusPedido. Reaproveita atualizar_status_pedido, sem
    duplicar a lógica de alteração de status/histórico. Não valida se o
    status atual permite cancelamento - essa regra fica para uma etapa
    futura.
    """
    return atualizar_status_pedido(db, pedido_id, StatusPedido.CANCELADO)
