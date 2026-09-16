# Projeto Delivery — Laticínio

Sistema web para automatizar o recebimento e gerenciamento de pedidos de
um laticínio de pequeno porte, com atendimento ao cliente via WhatsApp
e painel de gestão para o operador.

Status atual: **Fase 0 — estrutura inicial do projeto**, apenas com a
infraestrutura básica (FastAPI + configuração + conexão de banco +
Alembic configurado). Nenhuma regra de negócio foi implementada ainda.

## Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- Alembic (migrations)
- MySQL (driver PyMySQL)
- Pydantic v2 / pydantic-settings

## Como rodar localmente

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e ajuste com as credenciais do seu
   MySQL local:

   ```bash
   cp .env.example .env
   ```

4. Suba a aplicação:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Verifique se está no ar em `http://127.0.0.1:8000/health`.

## Estrutura do projeto

```
app/
├── main.py       - ponto de entrada da aplicação FastAPI
├── config.py      - leitura tipada das variáveis de ambiente
├── models/       - entidades do banco (SQLAlchemy) — vazio até a Fase 1
├── schemas/       - contratos de entrada/saída da API (Pydantic) — vazio até a Fase 1
├── routes/       - endpoints REST — vazio até a Fase 1
├── services/      - regras de negócio — vazio até a Fase 1
├── database/      - conexão/sessão com o MySQL
└── utils/        - funções auxiliares genéricas — vazio por enquanto

alembic/         - migrations do banco (configurado, sem migrations ainda)
tests/          - testes automatizados — vazio até a fase de testes
```

## Observações

- Nenhuma migration foi criada ainda. A primeira migration será gerada
  no início da Fase 1, depois que os models iniciais forem definidos.
- O `.env` deste repositório contém apenas placeholders e nunca deve
  ser versionado com credenciais reais (veja `.gitignore`).
