# 🛍️ API de Produtos Favoritos

API para gerenciar clientes e seus produtos favoritos, desenvolvida com FastAPI e armazenamento em memória.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg) ![Docker](https://img.shields.io/badge/Docker-compatible-blue.svg) ![Licença](https://img.shields.io/badge/license-MIT-brightgreen.svg)

## 📋 Índice

- [Requisitos](#-requisitos)
- [Execução Local](#-execução-local)
- [Docker](#-docker)
- [Testes](#-testes)
- [Endpoints](#-endpoints)
- [Qualidade de Código](#-qualidade-de-código)
- [Autenticação](#-autenticação)

## 🔧 Requisitos

- Python 3.11+
- FastAPI
- Uvicorn
- Docker

## 🚀 Execução Local

```bash
uvicorn apiluizalabs.main:app --port 8989 --reload
```

## 🐳 Docker

```bash
docker compose up --build
```

## 🧪 Testes

#### Para executar os testes (resultado resumido)
```bash
pytest
```

#### Para executar os testes com output (verboso)
```bash
pytest -v
```

#### Para executar os testes e mostrar cobertura de código
```bash
pytest --cov=apiluizalabs
```

#### Para executar os testes e mostrar cobertura de código em formato HTML
```bash
pytest --cov=apiluizalabs --cov-report=html
```
> O relatório estará disponível no diretório `htmlcov` (abra o arquivo `index.html`)

## 🌐 Endpoints

### Base

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Retorna mensagem de boas-vindas e links para documentação |
| GET | `/envs` | Lista todas as variáveis de ambiente (apenas para desenvolvimento) |
| GET | `/healthcheck` | Verifica se a API está funcionando corretamente |

### Clientes

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/clients/` | Lista todos os clientes cadastrados |
| GET | `/clients/{email}` | Retorna os dados de um cliente específico |
| POST | `/clients/` | Cria um novo cliente |
| PATCH | `/clients/{email}` | Atualiza os dados de um cliente existente |
| DELETE | `/clients/{email}` | Remove um cliente |

### Favoritos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/favorites/{email}` | Lista os produtos favoritos de um cliente |
| POST | `/favorites/{email}` | Adiciona um produto aos favoritos do cliente |
| DELETE | `/favorites/{email}/{product_id}` | Remove um produto dos favoritos do cliente |

### Produtos (Mock)
> Disponível apenas se `PRODUCTS_SOURCE=mock`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/products/` | Lista todos os produtos disponíveis (mockados) |
| GET | `/products/{product_id}` | Retorna detalhes de um produto específico |
| POST | `/products/mock/{total}` | Gera e adiciona produtos mockados para testes |

### Documentação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/docs` | Interface Swagger para explorar a API |
| GET | `/redoc` | Interface ReDoc para explorar a API |

## 🧹 Qualidade de código

Para manter a qualidade e o padrão de codificação, execute:

```bash
isort . && black .
```

> **isort**: Organiza as importações em ordem alfabética e por seções
> 
> **black**: Formata o código seguindo o padrão PEP 8

## 🔐 Autenticação

A API utiliza autenticação JWT. Para obter um token, faça uma requisição POST para `/token` com as credenciais de usuário:

- username=admin
- password=admin123

```bash
curl -X POST "http://localhost:8989/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Use o token retornado nas requisições subsequentes no cabeçalho Authorization:

```bash
curl -X GET "http://localhost:8989/clients/" \
  -H "Authorization: Bearer {seu_token_aqui}"
```

## 📝 Exemplos de Uso

### Criando um cliente
```bash
curl -X POST "http://localhost:8989/clients/" \
  -H "Authorization: Bearer {seu_token_aqui}" \
  -H "Content-Type: application/json" \
  -d '{"name": "João Silva", "email": "joao@email.com"}'
```

### Adicionando um produto aos favoritos
```bash
curl -X POST "http://localhost:8989/favorites/joao@email.com" \
  -H "Authorization: Bearer {seu_token_aqui}" \
  -H "Content-Type: application/json" \
  -d '{"id": "prod-000001"}'
```

---
Desenvolvido como parte do desafio técnico para Luiza Labs
