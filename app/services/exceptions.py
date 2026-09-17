class ErroNegocio(Exception):
    """
    Erro base para violação de regra de negócio.
    Mapeado pelas routes para HTTP 400 (Bad Request).
    """

    def __init__(self, mensagem: str):
        self.mensagem = mensagem
        super().__init__(mensagem)


class EntidadeNaoEncontrada(ErroNegocio):
    """
    Uma entidade relacionada (ex: cliente_id, bairro_id) não existe.
    Mapeado pelas routes para HTTP 404 (Not Found).
    """


class ConflitoDados(ErroNegocio):
    """
    Conflito de unicidade entre registros ativos (ex: telefone, nome).
    Mapeado pelas routes para HTTP 409 (Conflict).
    """
