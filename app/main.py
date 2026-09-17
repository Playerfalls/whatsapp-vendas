from fastapi import FastAPI

from app.routes import bairros, categorias, cidades, clientes, enderecos, produtos

app = FastAPI(
    title="Projeto Delivery - Laticínio",
    description=(
        "Sistema de automação de pedidos via WhatsApp com painel de "
        "gestão para um laticínio de pequeno porte."
    ),
    version="0.1.0",
)

app.include_router(clientes.router)
app.include_router(enderecos.router)
app.include_router(cidades.router)
app.include_router(bairros.router)
app.include_router(categorias.router)
app.include_router(produtos.router)


@app.get("/health")
def health_check():
    """
    Endpoint de verificação de saúde da aplicação.

    Não é uma rota de negócio - existe apenas para confirmarmos que o
    FastAPI está de pé (Fase 0). Rotas de negócio (produtos, pedidos
    etc.) serão adicionadas a partir da Fase 1, dentro de app/routes/.
    """
    return {"status": "ok"}
