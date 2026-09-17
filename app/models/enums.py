import enum


class StatusPedido(str, enum.Enum):
    """
    Status do pedido, conforme definido na especificação do projeto.
    Independente do status de pagamento (ver StatusPagamento).
    """

    NOVO = "NOVO"
    PREPARANDO = "PREPARANDO"
    PRONTO = "PRONTO"
    EM_ROTA = "EM_ROTA"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"
    RETORNADO = "RETORNADO"


class FormaPagamento(str, enum.Enum):
    """Forma de pagamento aprovada para o MVP (sem gateway real ainda)."""

    DINHEIRO = "DINHEIRO"
    PIX = "PIX"
    CARTAO = "CARTAO"


class StatusPagamento(str, enum.Enum):
    """Status do pagamento, aprovado para o MVP (registro manual, sem gateway)."""

    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    CANCELADO = "CANCELADO"
