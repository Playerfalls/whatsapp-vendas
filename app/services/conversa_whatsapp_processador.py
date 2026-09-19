from sqlalchemy.orm import Session

from app.models.enums import FormaPagamento
from app.schemas import pedido
from app.services import pedido_service
from app.services import produto_service
from app.services import carrinho_service
from app.models.conversa_whatsapp import ConversaWhatsapp
from app.services import conversa_whatsapp_service
from app.services import cliente_service
from app.schemas.cliente import ClienteCreate
from app.services import endereco_service
from app.services.conversa_whatsapp_estado import (
    ESTADO_CONFIRMAR_ENDERECO,
    ESTADO_CONFIRMAR_PEDIDO,
    ESTADO_IDENTIFICANDO_CLIENTE,
    ESTADO_INICIO,
    ESTADO_ESCOLHENDO_PRODUTOS,
    ESTADO_PEDIDO_CRIADO,
    ESTADO_ESCOLHER_PAGAMENTO,
    ESTADO_AGUARDANDO_DOCUMENTO,
)
from app.services.exceptions import ErroNegocio

def cliente_finalizou_produtos(mensagem: str) -> bool:
    mensagem_normalizada = mensagem.strip().lower()

    frases_finalizacao = {
        "não",
        "nao",
        "só isso",
        "so isso",
        "é só isso",
        "e só isso",
        "é isso",
        "e isso",
        "pode finalizar",
        "finalizar",
        "finaliza",
        "fechar pedido",
        "fechar",
    }

    return mensagem_normalizada in frases_finalizacao

def interpretar_confirmacao_pedido(mensagem: str) -> str:
    mensagem_normalizada = mensagem.strip().lower()

    confirmacoes = {
        "sim",
        "s",
        "confirmar",
        "confirmado",
        "pode confirmar",
        "pode fechar",
        "fechar pedido",
        "finalizar",
        "pode finalizar",
    }

    cancelamentos = {
        "não",
        "nao",
        "n",
        "cancelar",
        "cancela",
    }

    alteracoes = {
        "alterar",
        "editar",
        "mudar",
        "quero alterar",
        "quero editar",
    }

    if mensagem_normalizada in confirmacoes:
        return "CONFIRMAR"

    if mensagem_normalizada in cancelamentos:
        return "CANCELAR"

    if mensagem_normalizada in alteracoes:
        return "ALTERAR"

    return "NAO_IDENTIFICADO"

def processar_conversa(
    db: Session,
    conversa: ConversaWhatsapp,
    mensagem: str,
) -> str:

    if conversa.estado == ESTADO_INICIO:
        cliente = cliente_service.obter_cliente_por_telefone(
            db,
            conversa.telefone,
        )

        if cliente is not None:
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                "MENU",
            )

            return (
                f"Olá novamente, {cliente.nome}! 😊 "
                "Como posso te ajudar?"
            )

        conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
            "AGUARDANDO_NOME",
        )

        return (
            "Olá! 👋 Seja bem-vindo! "
            "Ainda não encontrei seu cadastro. "
            "Qual é o seu nome?"
        )

    if conversa.estado == ESTADO_IDENTIFICANDO_CLIENTE:
        cliente = cliente_service.obter_cliente_por_telefone(
            db,
            conversa.telefone,
        )

        if cliente is not None:
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                "MENU",
            )

            return (
                "Encontrei seu cadastro! 😊 "
                "Como posso te ajudar?"
            )

        conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
            "AGUARDANDO_NOME",
        )

        return (
            "Ainda não encontrei seu cadastro. "
            "Qual é o seu nome?"
        )

    if conversa.estado == "AGUARDANDO_NOME":
        nome = mensagem.strip()

        if not nome:
            return "Por favor, informe seu nome."

        cliente = cliente_service.criar_cliente(
            db,
            ClienteCreate(
                nome=nome,
                telefone=conversa.telefone,
            ),
        )

        conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
            "MENU",
        )

        return (
            f"Prazer, {cliente.nome}! 😊 "
            "Seu cadastro foi realizado. "
            "Como posso te ajudar?"
        )

    if conversa.estado == ESTADO_AGUARDANDO_DOCUMENTO:
        cliente = cliente_service.obter_cliente_por_telefone(
        db,
        conversa.telefone,
    )

        if cliente is None:
            return (
                "Não consegui localizar seu cadastro. "
                "Vamos precisar refazer o cadastro."
        )

        try:
            cpf_cnpj = cliente_service.normalizar_cpf_cnpj(
                mensagem,
        )
        except ErroNegocio:
            return (
                "CPF ou CNPJ inválido. 🤔\n\n"
                "Digite um CPF com 11 dígitos "
                "ou um CNPJ com 14 dígitos."
        )

        cliente.cpf_cnpj = cpf_cnpj
        db.commit()
        db.refresh(cliente)

        conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
             ESTADO_ESCOLHER_PAGAMENTO,
    )

        return (
            "CPF/CNPJ cadastrado com sucesso! ✅\n\n"
            "Agora escolha a forma de pagamento:\n\n"
            "1️⃣ Dinheiro\n"
            "2️⃣ PIX\n"
            "3️⃣ Cartão"
    )

    if conversa.estado == "MENU":
        mensagem_normalizada = mensagem.strip().lower()

        if (
            "consultar" in mensagem_normalizada
            or "status" in mensagem_normalizada
        ):
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                "CONSULTANDO_PEDIDO",
            )

            return (
                "Claro! 🔎 "
                "Vou consultar seu pedido."
            )

        if (
            "pedido" in mensagem_normalizada
            or "comprar" in mensagem_normalizada
        ):
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                "ESCOLHENDO_PRODUTOS",
            )

            catalogo = produto_service.listar_catalogo(db)

            return produto_service.formatar_catalogo(catalogo)

        if (
            "atendente" in mensagem_normalizada
            or "humano" in mensagem_normalizada
        ):
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                "ATENDIMENTO_HUMANO",
            )

            return (
                "Certo! 👤 "
                "Vou encaminhar você para um atendente."
            )

            return (
            "Olá! 😊 Como posso te ajudar?\n\n"
            "1️⃣ Fazer um pedido\n"
            "2️⃣ Consultar pedido\n"
            "3️⃣ Falar com atendente"
        )

    if conversa.estado == ESTADO_ESCOLHENDO_PRODUTOS:
        if cliente_finalizou_produtos(mensagem):
            carrinho = carrinho_service.obter_ou_criar_carrinho(
                db,
                conversa,
            )

            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                ESTADO_CONFIRMAR_PEDIDO,
            )

            return carrinho_service.formatar_resumo(
                db,
                carrinho,
            )

        resultado = produto_service.interpretar_item_pedido(
            db,
            mensagem,
        )

        if resultado["status"] == "AMBIGUO":
            return (
                "Encontrei mais de uma opção para esse produto. "
                "Qual você deseja?"
            )

        if resultado["status"] == "QUANTIDADE_INVALIDA":
            return (
                "A quantidade informada não é válida. "
                "Por favor, informe uma quantidade maior que zero."
            )

        if resultado["status"] == "NAO_ENCONTRADO":
            return (
                "Não encontrei esse produto no nosso catálogo. "
                "Por favor, tente novamente."
            )

        produto = resultado["produto"]
        quantidade = resultado["quantidade"]

        carrinho = carrinho_service.obter_ou_criar_carrinho(
            db,
            conversa,
        )

        try:
            carrinho_service.adicionar_item(
                db,
                carrinho,
                produto,
                quantidade,
            )
        except ValueError as erro:
            return str(erro)

        return (
            f"✅ Adicionei {quantidade}x {produto.nome} ao seu pedido.\n\n"
            "Deseja adicionar mais alguma coisa?"
        )

    if conversa.estado == ESTADO_CONFIRMAR_PEDIDO:
        resultado = interpretar_confirmacao_pedido(mensagem)

        if resultado == "CONFIRMAR":
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                ESTADO_CONFIRMAR_ENDERECO,
    )

            return (
                "Pedido confirmado! ✅\n\n"
                "Agora vamos confirmar seu endereço de entrega. 📍"
    )

        if resultado == "CANCELAR":
            carrinho_service.limpar_carrinho(
                db,
                carrinho_service.obter_ou_criar_carrinho(
                    db,
                    conversa,
                ),
            )

            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                "MENU",
            )

            return (
                "Tudo bem! 👍 "
                "O pedido foi cancelado.\n\n"
                "Como posso te ajudar?"
            )

        if resultado == "ALTERAR":
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                ESTADO_ESCOLHENDO_PRODUTOS,
            )

            return (
                "Claro! 🛒 "
                "Você pode adicionar, remover ou alterar "
                "os produtos do seu pedido."
            )

        return (
            "Não entendi. 🤔\n\n"
            "Por favor, responda:\n"
            "✅ Sim, para confirmar\n"
            "❌ Não, para cancelar\n"
            "✏️ Alterar, para modificar o pedido."
        )

    if conversa.estado == ESTADO_CONFIRMAR_ENDERECO:
        cliente = cliente_service.obter_cliente_por_telefone(
            db,
            conversa.telefone,
        )

        if cliente is None:
            return (
                "Não consegui localizar seu cadastro. "
                "Vamos precisar refazer o cadastro."
            )

        enderecos = endereco_service.listar_enderecos_do_cliente(
            db,
            cliente.id,
        )

        if not enderecos:
            return (
                "Você ainda não possui um endereço de entrega cadastrado. 📍\n\n"
                "Precisamos cadastrar um endereço antes de continuar."
            )

        mensagem_normalizada = mensagem.strip().lower()

        # Cliente possui apenas um endereço
        if len(enderecos) == 1:
            endereco = enderecos[0]

            if mensagem_normalizada in {"sim", "s", "confirmar"}:
                conversa.endereco_id = endereco.id

                conversa_whatsapp_service.alterar_estado(
                    db,
                    conversa,
                    "ESCOLHENDO_PAGAMENTO",
                )

                return (
                    "Endereço confirmado! 📍✅\n\n"
                    "Agora escolha a forma de pagamento:\n\n"
                    "1️⃣ Dinheiro\n"
                    "2️⃣ PIX\n"
                    "3️⃣ Cartão"
                )

            if mensagem_normalizada in {"não", "nao", "n"}:
                return (
                    "Tudo bem! 📍\n\n"
                    "Precisamos cadastrar ou selecionar outro endereço "
                    "antes de continuar."
                )

            return (
                "Não entendi. 🤔\n\n"
                "Responda SIM para confirmar o endereço "
                "ou NÃO para informar que deseja outro."
            )

        # Cliente possui vários endereços
        try:
            indice = int(mensagem_normalizada)
        except ValueError:
            return (
                "Por favor, informe o número do endereço "
                "que deseja utilizar."
            )

        if indice < 1 or indice > len(enderecos):
            return (
                "Esse número de endereço não é válido. 🤔\n\n"
                "Por favor, escolha um dos números apresentados."
            )

        endereco = enderecos[indice - 1]

        conversa.endereco_id = endereco.id

        conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
            "ESCOLHENDO_PAGAMENTO",
        )

        return (
            "Endereço selecionado! 📍✅\n\n"
            "Agora escolha a forma de pagamento:\n\n"
            "1️⃣ Dinheiro\n"
            "2️⃣ PIX\n"
            "3️⃣ Cartão"
        )
    
    if conversa.estado == ESTADO_ESCOLHER_PAGAMENTO:
        mensagem_normalizada = mensagem.strip().lower()

        formas_pagamento = {
            "1": FormaPagamento.DINHEIRO,
            "2": FormaPagamento.PIX,
            "3": FormaPagamento.CARTAO,
        }

        forma_pagamento = formas_pagamento.get(mensagem_normalizada)

        if forma_pagamento is None:
            return (
                "Não entendi a forma de pagamento. 🤔\n\n"
                "Escolha uma das opções:\n\n"
                "1️⃣ Dinheiro\n"
                "2️⃣ PIX\n"
                "3️⃣ Cartão"
            )
    conversa.forma_pagamento = forma_pagamento.value

    if forma_pagamento == FormaPagamento.PIX:
        cliente = cliente_service.obter_cliente_por_telefone(
            db,
            conversa.telefone,
        )

        if cliente is None:
            return (
                "Não consegui localizar seu cadastro. "
                "Vamos precisar refazer o cadastro."
            )

        if not cliente.cpf_cnpj:
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                ESTADO_AGUARDANDO_DOCUMENTO,
            )

            return (
                "Para realizar o pagamento via PIX, precisamos "
                "do seu CPF ou CNPJ. 🔐\n\n"
                "Digite apenas o CPF ou CNPJ."
        )
        

        conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
            ESTADO_PEDIDO_CRIADO,
)

        return (
            f"Pedido #{pedido.id} criado com sucesso! 🎉\n\n"
            f"💰 Total: R$ {pedido.valor_total:.2f}\n"
            f"💳 Pagamento: {forma_pagamento.value}"
        )

    if conversa.estado == "CONSULTANDO_PEDIDO":
        cliente = cliente_service.obter_cliente_por_telefone(
            db,
            conversa.telefone,
    )

        if cliente is None:
            return (
            "Não consegui localizar seu cadastro. "
            "Vamos precisar refazer o cadastro."
        )

        pedidos = pedido_service.listar_pedidos_do_cliente(
            db,
            cliente.id,
            limit=1,
    )

        if not pedidos:
            conversa_whatsapp_service.alterar_estado(
                db,
                conversa,
                "MENU",
        )

            return (
                "Você ainda não possui pedidos registrados. 📦\n\n"
                "Como posso te ajudar?"
        )

        pedido = pedidos[0]

        conversa_whatsapp_service.alterar_estado(
            db,
            conversa,
            "MENU",
    )

        return (
            f"📦 Pedido #{pedido.id}\n\n"
            f"📌 Status: {pedido.status.value}\n"
            f"💰 Total: R$ {pedido.valor_total:.2f}\n"
            f"💳 Pagamento: {pedido.pagamento.forma_pagamento.value}\n\n"
            "Como posso te ajudar?"
    )
    
    return "Mensagem recebida."

