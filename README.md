# Search API for Developers

Uma API de busca, construída com Python e FastAPI, para ajudar desenvolvedores a encontrar soluções para problemas técnicos em sites de referência.

## Funcionalidades (MVP)

- Endpoint `GET /api/v1/search`.
- Busca por texto livre (`query`).
- Provider inicial: **Stack Overflow** (via API oficial).
- Estrutura modular e assíncrona, pronta para expansão.
- Ranking inicial simples baseado em popularidade e peso da fonte.
- Retry automático para requisições externas.
- Logging estruturado com Loguru.

## Como Executar

### 1. Pré-requisitos

- Python 3.11+
- Poetry (recomendado) ou pip

### 2. Instalação

Clone o repositório e instale as dependências:

```bash
git clone <url-do-seu-repositorio>
cd search-api
pip install -r requirements.txt
```

### 3. Configuração

Copie o arquivo de exemplo `.env.example` para `.env` e adicione sua chave da API do Stack Exchange (opcional, mas recomendado para aumentar o limite de requisições).

```bash
cp .env.example .env
```

### 4. Executando o Servidor

Use o Uvicorn para iniciar a aplicação:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000/docs`.
