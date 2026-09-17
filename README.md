# WhatsApp Vendas

Backend para gerenciamento de pedidos e vendas integrado ao WhatsApp, desenvolvido como projeto de estudo e portfólio profissional.

O projeto está sendo construído de forma incremental, com foco em boas práticas de desenvolvimento backend, organização de código, modelagem de dados, APIs e persistência em banco de dados.

## Status do projeto

**Fase 1 — Modelagem inicial do banco de dados e configuração das migrations.**

A estrutura inicial da aplicação foi implementada e o banco de dados MySQL está configurado através do SQLAlchemy e Alembic.

Nesta fase foram criados os modelos iniciais do sistema, seus relacionamentos e a primeira migration, que já foi aplicada ao banco de dados.

O desenvolvimento seguirá de forma incremental nas próximas fases.

## Tecnologias utilizadas

* Python
* FastAPI
* SQLAlchemy 2.0
* Alembic
* MySQL
* PyMySQL
* Pydantic
* Pydantic Settings
* Uvicorn
* Git
* GitHub

## Estrutura do projeto

```text
projeto-delivery/
├── alembic/
│   ├── versions/
│   │   ├── .gitkeep
│   │   └── 27e1178a903d_criacao_tabelas_iniciais.py
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── bairro.py
│   │   ├── categoria.py
│   │   ├── cidade.py
│   │   ├── cliente.py
│   │   ├── endereco.py
│   │   ├── enums.py
│   │   ├── historico_status_pedido.py
│   │   ├── item_pedido.py
│   │   ├── pagamento.py
│   │   ├── pedido.py
│   │   ├── produto.py
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── routes/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/
│   └── .gitkeep
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

> O arquivo `.env` é utilizado apenas no ambiente local e não deve ser versionado no Git. O `.env.example` serve como modelo de configuração.

## Modelagem atual

O banco de dados possui atualmente as seguintes entidades:

* `cidades`
* `bairros`
* `categorias`
* `produtos`
* `clientes`
* `enderecos`
* `pedidos`
* `itens_pedido`
* `pagamentos`
* `historico_status_pedido`

Além dessas tabelas, o Alembic utiliza a tabela `alembic_version` para controlar a versão das migrations aplicadas.

### Principais relacionamentos

* Uma cidade possui vários bairros.
* Uma categoria possui vários produtos.
* Um cliente pode possuir vários endereços.
* Um bairro pode estar associado a vários endereços.
* Um cliente pode possuir vários pedidos.
* Um pedido pode possuir vários itens.
* Um produto pode aparecer em vários itens de pedidos.
* Um pedido possui um pagamento.
* Um pedido possui um histórico de alterações de status.

### Regras importantes

* Produtos, categorias, bairros e cidades possuem controle de ativação para permitir exclusão lógica.
* Clientes e endereços também possuem controle de ativação.
* O pedido mantém um snapshot do endereço utilizado na entrega para preservar o histórico.
* O preço unitário e o subtotal dos itens são armazenados no pedido para preservar os valores históricos.
* O status do pedido é separado do status do pagamento.
* Um pedido possui no máximo um pagamento.

## Banco de dados

O projeto utiliza **MySQL** como banco de dados.

As migrations são gerenciadas pelo **Alembic**, permitindo controlar a evolução do schema do banco de forma versionada.

A primeira migration foi criada e aplicada com sucesso ao banco de dados.

## Configuração do ambiente

Clone o repositório e crie um ambiente virtual Python:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` baseado no `.env.example` e informe as credenciais do seu ambiente MySQL.

Exemplo:

```env
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=delivery
```

## Migrations

Para verificar a migration atualmente aplicada:

```bash
alembic current
```

Para aplicar migrations pendentes:

```bash
alembic upgrade head
```

## Execução da aplicação

Para iniciar a aplicação em ambiente de desenvolvimento:

```bash
uvicorn app.main:app --reload
```

A aplicação possui atualmente um endpoint de verificação:

```text
GET /health
```

## Desenvolvimento

O projeto está sendo desenvolvido por fases, priorizando primeiro a estrutura e a infraestrutura do backend antes da implementação das regras de negócio.

As próximas etapas serão adicionadas gradualmente, incluindo as camadas de schemas, serviços, rotas e funcionalidades do sistema.

## Observações

* O projeto ainda está em desenvolvimento.
* O frontend ainda não faz parte desta etapa do projeto.
* Integrações externas, como WhatsApp e pagamentos, serão implementadas em fases posteriores.
* O `.env` contém informações específicas do ambiente local e não deve ser versionado.
* O `.env.example` deve ser utilizado como referência para configuração do ambiente.
* As decisões de arquitetura e implementação serão evoluídas conforme os requisitos das próximas fases.
