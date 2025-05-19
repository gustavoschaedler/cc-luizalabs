# 🏆 Desafio Técnico - Luiza Labs

## 🛍️ API de Produtos Favoritos

API para gerenciar clientes e seus produtos favoritos, desenvolvida com FastAPI e armazenamento em memória.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg) ![Docker](https://img.shields.io/badge/Docker-compatible-blue.svg) ![Cobertura](https://img.shields.io/badge/Cobertura-90%25-brightgreen.svg) ![Licença](https://img.shields.io/badge/license-MIT-brightgreen.svg)

## 📋 Índice

- [Cenário](#-cenário)
- [Escopo](#-escopo)
- [URL Externa da API](#-url-externa-da-api)
- [Documentação Online](#-documentação-online)
- [TL;DR](#-tldr)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Aliases](#-aliases)
- [Padrão Arquitetural](#-padrão-arquitetural)
- [Requisitos](#-requisitos)
- [Execução Local](#-execução-local)
- [Docker](#-docker)
- [Testes](#-testes)
- [Endpoints](#-endpoints)
- [Qualidade de Código](#-qualidade-de-código)
- [Autenticação](#-autenticação)


## 📜 Cenário

O **Magalu** está expandindo seus negócios e uma das novas missões do time de tecnologia é criar uma funcionalidade de **Produtos Favoritos** para nossos Clientes. Nesta funcionalidade, nossos aplicativos enviarão requisições HTTP para um novo backend que gerenciará nossos clientes e seus produtos favoritos.

Esta nova API REST será **crucial para as ações de marketing** da empresa e terá um **grande volume de requisições**, então a preocupação com performance é constante em nosso desenvolvimento.

## ✅ Escopo

### Clientes
- Deve ser possível criar, atualizar, visualizar e remover Clientes
  - O cadastro dos clientes deve conter apenas seu nome e endereço de e-mail
  - Um cliente não pode se registrar duas vezes com o mesmo endereço de e-mail

### Produtos Favoritos
- Cada cliente só deverá ter uma única lista de produtos favoritos
- Em uma lista de produtos favoritos podem existir uma quantidade ilimitada de produtos
  - Um produto não pode ser adicionado em uma lista caso ele não exista
  - Um produto não pode estar duplicado na lista de produtos favoritos de um cliente
  - A documentação da API de produtos pode ser visualizada [neste link](https://gist.github.com/Bgouveia/9e043a3eba439489a35e70d1b5ea08ec)

### Renderização
- O dispositivo que irá renderizar a resposta fornecida por essa nova API irá apresentar:
  - Título
  - Imagem
  - Preço
  - ID do produto (para formatar o link de acesso)
  - Review do produto (quando existir)
- Não é necessário criar um frontend para simular essa renderização (foque no desenvolvimento da API)

### Segurança
- O acesso à API deve ser aberto ao mundo, porém deve possuir autenticação e autorização

### Banco de Dados
- Não utilizar banco de dados relacional ou NoSQL
- Utilizar um banco de dados em memória (estrutura de dados) para armazenar os dados

## 🌍 URL Externa da API

A API está disponível publicamente no seguinte endereço: **[https://apiluizalabs.audiencesdata.uk/](https://apiluizalabs.audiencesdata.uk/)**

### Hardware

Esta API esta rodando em uma Virtual Machine (VM) Ubuntu Server instalada em um servidor local na minha casa virtualizada via ProxMox.
A exposição da API foi feita via Tunnels do Cloudflare.

### Documentação Online

Para explorar a API através da interface Swagger UI, acesse:
- [Documentação Swagger](https://apiluizalabs.audiencesdata.uk/docs)
- [Documentação ReDoc](https://apiluizalabs.audiencesdata.uk/redoc)

## 🚀 TL;DR

### Implantação Rápida

### Via Docker
```bash
git clone https://github.com/gustavoschaedler/cc-luizalabs.git
cd cc-luizalabs
cp .env.example .env
docker compose up --build
```
🔗 Então acesse: **[http://0.0.0.0:8989](http://0.0.0.0:8989)**

### Localmente
```bash
git clone https://github.com/gustavoschaedler/cc-luizalabs.git
cd cc-luizalabs
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn apiluizalabs.main:app --port 8989 --reload
```
🔗 Então acesse: **[http://localhost:8989](http://localhost:8989)**

## ⚙️ Variáveis de Ambiente

Configure a aplicação através do arquivo `.env` (use `.env.example` como modelo):

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `SECRET_KEY` | Chave secreta para assinar os tokens JWT | `sua_chave_secreta_aqui` |
| `ALGORITHM` | Algoritmo de assinatura JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token JWT (em minutos) | `60` |
| `PRODUCTS_SOURCE` | Define a origem dos produtos (`mock` ou `api`) | `mock` |
| `PRODUCTS_API_URL` | URL da API de produtos (apenas se `PRODUCTS_SOURCE=api`) | - |

> **Nota**: Para ambiente de produção, certifique-se de definir uma `SECRET_KEY` forte, segura e aleatória.
---

# 🛠️ Aliases para Desenvolvimento

Para facilitar o desenvolvimento e execução de tarefas comuns, o projeto inclui um arquivo de aliases que pode ser carregado no seu ambiente bash. Estes aliases fornecem atalhos para comandos frequentemente utilizados.

## 📋 Aliases Disponíveis

Adicione os seguintes aliases ao seu ambiente carregando o arquivo:

```bash
source aliases
```

| Alias | Comando | Descrição |
|-------|---------|-----------|
| `db` | `docker-compose build` | Constrói os containers Docker |
| `dup` | `docker-compose up` | Inicia os containers Docker |
| `dbnocache` | `docker-compose build --no-cache` | Constrói os containers sem utilizar cache |
| `run` | `uvicorn apiluizalabs.main:app --port 8989 --reload` | Inicia a aplicação localmente com hot-reload |
| `testv` | `pytest -v` | Executa os testes com saída detalhada (verbose) |
| `testcov` | `pytest --cov=apiluizalabs` | Executa os testes com relatório de cobertura |
| `testcovhtml` | `pytest --cov=apiluizalabs --cov-report=html` | Gera relatório de cobertura em HTML |

## 🚀 Exemplos de Uso

Para iniciar a aplicação localmente:
```bash
run
```

Para executar os testes com relatório de cobertura:
```bash
testcov
```

Para construir e iniciar os containers Docker:
```bash
db && dup
```

Estes aliases economizam tempo durante o desenvolvimento, permitindo executar comandos complexos com poucos caracteres.

---

## 🏗️ Padrão Arquitetural

O projeto segue o padrão **Service-Repository**:

- **Rotas (Routes):** Camada responsável por definir os endpoints da API, utilizando o FastAPI para receber requisições HTTP e delegar a lógica para os serviços.
- **Serviços (Services):** Camada intermediária que concentra a lógica de negócio, validações e orquestração entre repositórios e utils (ex: cache).
- **Repositórios (Repositories):** Responsáveis pelo acesso e manipulação dos dados, seja em memória, mock ou via API externa.
- **Utilitários (Utils):** Componentes auxiliares, como o cache LRU com TTL para otimizar buscas.
- **Autenticação:** Implementada via OAuth2 com JWT, protegendo as rotas que necessitam de autorização.

Neste padrão há separação de responsabilidades, facilitando manutenção, testes e escalabilidade.

---

### 📂 Estrutura de pastas
```
.
├── aliases
├── apiluizalabs
│   ├── __init__.py
│   ├── auth.py
│   ├── main.py
│   ├── models.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── client_repository.py
│   │   ├── favorite_repository.py
│   │   └── product_repository.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── clients.py
│   │   ├── favorites.py
│   │   └── products.py
│   ├── schemas.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── client_service.py
│   │   ├── favorite_service.py
│   │   └── product_service.py
│   └── utils
│       ├── __init__.py
│       └── cache.py
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    ├── test_clients.py
    ├── test_favorites.py
    ├── test_main.py
    ├── test_product_service.py
    └── test_products.py
```

**Resumo:**  
- FastAPI para rotas e documentação automática  
- Service-Repository para lógica e persistência  
- Cache LRU TTL para otimização  
- Autenticação JWT  
- Testes automatizados com pytest


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

### Root
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Retorna mensagem de boas vindas e links para documentação |

### Debug
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/envs` | Lista todas as variáveis de ambiente (apenas para desenvolvimento) |

### DevOps
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/healthcheck` | Verifica saúde da API (retorna "ok" se estiver online) |

### Autenticacao

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/token` | Gera o access_token para ser utilizado na autorizacao |

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
