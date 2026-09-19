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

def criar_cobranca_pix(
    customer_id: str,
    valor: float,
    descricao: str,
    external_reference: str | None = None,
    due_date: str | None = None,
) -> dict:
    
    dados = {
    "customer": customer_id,
    "billingType": "PIX",
    "value": valor,
    "description": descricao,
}

    if due_date:
        dados["dueDate"] = due_date

    if external_reference:
        dados["externalReference"] = external_reference

    resposta = requests.post(
        f"{settings.asaas_base_url}/payments",
        headers=_headers(),
        json=dados,
        timeout=30,
    )

    if not resposta.ok:
        raise ValueError(
        f"Erro ao criar cobrança PIX no Asaas: "
        f"{resposta.status_code} - {resposta.text}"
    )

    return resposta.json()  

def obter_qr_code_pix(payment_id: str) -> dict:
    resposta = requests.get(
        f"{settings.asaas_base_url}/payments/{payment_id}/pixQrCode",
        headers=_headers(),
        timeout=30,
    )

    if not resposta.ok:
        raise ValueError(
            f"Erro ao obter QR Code PIX no Asaas: "
            f"{resposta.status_code} - {resposta.text}"
        )

    return resposta.json()