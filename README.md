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
Para executar os testes (resultado resumido).

```bash
pytest -v
```
Para executar os testes com output (verboso).

```bash
pytest --cov=app
```
Para executar os testes e mostrar cobertura de codigo.

```bash
pytest --cov=app --cov-report=html
```
Para executar os testes e mostrar cobertura de codigo em formato HTML, disponivel depois no diretorio htmlcov (index.html).

## Endpoints

### Base

- **GET /**  
  Retorna mensagem de ola mundo + links para a documentacao/pagina Swagger e ReDoc.

- **GET /envs**  
  Lista todas as variaveis de ambiente carregadas no ambiente da aplicacao (para dev apenas).

- **GET /healthcheck**  
  "PING" Verifica se a API está rodando corretamente (retorna {"status": "ok"}).

### Clientes

- **GET /clients/**  
  Lista todos os clientes cadastrados.

- **GET /clients/{email}**  
  Retorna os dados de um cliente especifico pelo email.

- **POST /clients/**  
  Cria um novo cliente.

- **PATCH /clients/{email}**  
  Atualiza os dados de um cliente existente.

- **DELETE /clients/{email}**  
  Remove um cliente pelo email.

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
  Lista todos os produtos disponiveis (mockados).

- **GET /products/{product_id}**  
  Retorna detalhes de um produto especifico (mockado).

- **POST /products/mock/{total}**  
  Gera e adiciona produtos mockados (apenas modo mock - proposito de testes).

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
  Swagger para exploração da API
- [GET] /redoc
  ReDoc para exploracao da API

