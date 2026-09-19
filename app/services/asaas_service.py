import requests

from app.config import settings


def _headers() -> dict:
    return {
        "access_token": settings.asaas_api_key,
        "Content-Type": "application/json",
        "User-Agent": "whatsapp-vendas",
    }


def criar_cliente(
    nome: str,
    telefone: str,
    cpf_cnpj: str | None = None,
) -> dict:
    dados = {
        "name": nome,
        "mobilePhone": telefone,
    }

    if cpf_cnpj:
        dados["cpfCnpj"] = cpf_cnpj

    resposta = requests.post(
        f"{settings.asaas_base_url}/customers",
        headers=_headers(),
        json=dados,
        timeout=30,
    )

    resposta.raise_for_status()

    return resposta.json()