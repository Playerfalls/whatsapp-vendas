# Projeto Delivery - Laticínio

Sistema de automação e gerenciamento de pedidos desenvolvido para um laticínio de pequeno porte, com foco em uma futura integração com pedidos via WhatsApp e disponibilização de uma API para gerenciamento das informações do sistema.

> **Status:** Em desenvolvimento — Fase 2 concluída.

---

## 📌 Sobre o projeto

Este projeto está sendo desenvolvido como uma aplicação backend para automatizar e organizar o fluxo de pedidos de um laticínio.

A aplicação está sendo construída utilizando **Python** e **FastAPI**, com persistência de dados através de **SQLAlchemy** e gerenciamento de alterações do banco de dados utilizando **Alembic**.

A arquitetura está sendo desenvolvida de forma modular, separando responsabilidades entre banco de dados, modelos, schemas, rotas, serviços e utilitários.

O projeto será evoluído gradualmente, adicionando as funcionalidades necessárias para chegar à automação completa do processo de pedidos.

---

## 🚧 Status atual

### Fase 1 — Estrutura e base do projeto

* [x] Estrutura inicial do projeto
* [x] Configuração do ambiente virtual
* [x] Configuração do FastAPI
* [x] Configuração do Uvicorn
* [x] Configuração do SQLAlchemy
* [x] Configuração do Alembic
* [x] Configuração de conexão com banco de dados
* [x] Estrutura inicial de models
* [x] Organização modular da aplicação

### Fase 2 — Schemas

* [x] Criação dos schemas Pydantic
* [x] Schema de Bairro
* [x] Schema de Categoria
* [x] Schema de Cidade
* [x] Schema de Cliente
* [x] Schema de Endereço
* [x] Schema de Item de Pedido
* [x] Schema de Pagamento
* [x] Schema de Pedido
* [x] Schema de Produto
* [x] Validação de sintaxe dos novos arquivos
* [x] Validação dos imports dos schemas
* [x] Validação da inicialização da aplicação
* [x] Documentação automática via Swagger/OpenAPI

### Próximas etapas

As próximas fases serão responsáveis pela implementação gradual das regras de negócio, endpoints da API, serviços e demais funcionalidades do sistema.

---

## 🛠️ Tecnologias utilizadas

* **Python 3.11**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy**
* **Alembic**
* **PyMySQL**
* **Uvicorn**
* **python-dotenv**
* **Requests**
* **Pandas**
* **NumPy**
* **Pytest**
* **Git / GitHub**

---

## 📁 Estrutura atual

```text
whatsapp-vendas/
│
├── alembic/
│
├── app/
│   ├── database/
│   │   └── session.py
│   │
│   ├── models/
│   │
│   ├── routes/
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── bairro.py
│   │   ├── categoria.py
│   │   ├── cidade.py
│   │   ├── cliente.py
│   │   ├── endereco.py
│   │   ├── item_pedido.py
│   │   ├── pagamento.py
│   │   ├── pedido.py
│   │   └── produto.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   └── __init__.py
│   │
│   └── main.py
│
├── venv/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> A estrutura será expandida conforme novas funcionalidades forem implementadas.

---

## ⚙️ Configuração do ambiente

### 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
```

Depois, entre na pasta:

```bash
cd whatsapp-vendas
```

### 2. Criar o ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

---

## 🔐 Variáveis de ambiente

As configurações sensíveis da aplicação devem ser armazenadas em um arquivo `.env`.

O arquivo `.env` **não deve ser versionado no Git**, pois pode conter credenciais e informações de acesso ao banco de dados.

Um exemplo de configuração pode ser criado em um arquivo `.env.example` futuramente.

---

## ▶️ Executando a aplicação

Com o ambiente virtual ativado:

```bash
uvicorn app.main:app --reload
```

A aplicação será disponibilizada localmente em:

```text
http://127.0.0.1:8000
```

---

## 📚 Documentação da API

O FastAPI disponibiliza automaticamente a documentação interativa da aplicação.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### OpenAPI

```text
http://127.0.0.1:8000/openapi.json
```

Atualmente, a documentação da API ainda possui poucos endpoints, pois as rotas da aplicação serão implementadas nas próximas fases do projeto.

---

## 🧪 Testes

O projeto já possui o **Pytest** configurado como ferramenta de testes.

Para executar os testes:

```bash
python -m pytest
```

No momento, os testes automatizados ainda estão sendo estruturados.

---

## 🗄️ Banco de dados

O projeto utiliza:

* **SQLAlchemy** para interação com o banco de dados;
* **Alembic** para gerenciamento de migrations;
* **PyMySQL** para conexão com bancos MySQL.

A estrutura do banco será ampliada conforme os models e regras de negócio forem implementados.

---

## 🏗️ Arquitetura

A aplicação está sendo organizada de maneira modular para separar as responsabilidades de cada parte do sistema:

```text
app/
│
├── database/    → Configurações e conexão com o banco
├── models/      → Modelos das entidades
├── schemas/     → Validação e serialização dos dados
├── routes/      → Endpoints da API
├── services/    → Regras de negócio
└── utils/       → Funções auxiliares
```

Essa separação permite que novas funcionalidades sejam adicionadas de maneira organizada conforme o projeto evolui.

---

## 🎯 Objetivo futuro

O objetivo final do projeto é criar uma solução capaz de auxiliar na automação do processo de vendas de um pequeno laticínio, centralizando informações de clientes, produtos e pedidos e permitindo a evolução para uma integração com WhatsApp.

As funcionalidades serão implementadas progressivamente durante o desenvolvimento do projeto.

---

## 👨‍💻 Desenvolvimento

Projeto desenvolvido como parte de um projeto prático de desenvolvimento backend utilizando Python.

O desenvolvimento também tem como objetivo aplicar na prática conceitos de:

* Python
* APIs REST
* FastAPI
* Pydantic
* SQL
* SQLAlchemy
* MySQL
* Alembic
* Git e GitHub
* Testes automatizados

---

## 📄 Licença

Este projeto está em desenvolvimento. A definição da licença será realizada posteriormente, conforme a finalidade de distribuição do projeto.
