# API de Produtos Favoritos

API para gerenciar clientes e seus produtos favoritos.
Dados armazenados em memória. Framework utilzado FastAPI.

## Requisitos

- Python 3.11+
- FastAPI
- Uvicorn

## Execução Local

```bash
uvicorn app.main:app --port 8989 --reload
```

## Docker

```bash
docker-compose up --build
```

## Testes

```bash
pytest
```

## Endpoints

### Base

- **GET /**  
  Retorna mensagem de boas-vindas e links para a documentação Swagger e ReDoc.

- **GET /envs**  
  Lista todas as variáveis de ambiente carregadas no ambiente da aplicação.

- **GET /healthcheck**  
  Verifica se a API está rodando corretamente (retorna {"status": "ok"}).

### Clientes

- **GET /clients/**  
  Lista todos os clientes cadastrados.

- **GET /clients/{email}**  
  Retorna os dados de um cliente específico pelo e-mail.

- **POST /clients/**  
  Cria um novo cliente.

- **PATCH /clients/{email}**  
  Atualiza os dados de um cliente existente.

- **DELETE /clients/{email}**  
  Remove um cliente pelo e-mail.

### Favoritos

- **GET /favorites/{email}**  
  Lista os produtos favoritos de um cliente.

- **POST /favorites/{email}**  
  Adiciona um produto aos favoritos do cliente.

- **DELETE /favorites/{email}/{product_id}**  
  Remove um produto dos favoritos do cliente.

### Produtos (Mock)
> Disponível apenas se `PRODUCTS_SOURCE=mock`

- **GET /products/**  
  Lista todos os produtos disponíveis (mockados).

- **GET /products/{product_id}**  
  Retorna detalhes de um produto específico (mockado).

- **POST /products/mock/{total}**  
  Gera e adiciona produtos mockados (apenas modo mock).

### Documentação

- **GET /docs**  
  Interface Swagger para explorar a API.

- **GET /redoc**  
  Interface ReDoc para explorar a API.

## Qualidade de código
```bash
black . && isort .
```

## Documentação / Swagger

- [GET] /docs
- [GET] /redoc

