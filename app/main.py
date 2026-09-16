from fastapi import FastAPI

app = FastAPI(
    title="Projeto Delivery - Laticínio",
    description=(
        "Sistema de automação de pedidos via WhatsApp com painel de "
        "gestão para um laticínio de pequeno porte."
    ),
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """
    Endpoint de verificação de saúde da aplicação.

    Não é uma rota de negócio - existe apenas para confirmarmos que o
    FastAPI está de pé (Fase 0). Rotas de negócio (produtos, pedidos
    etc.) serão adicionadas a partir da Fase 1, dentro de app/routes/.
    """
    return {"status": "ok"}
