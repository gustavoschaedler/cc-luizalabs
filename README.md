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

- [GET] /clientes
- [GET] /clientes/{cliente_id}
- [POST] /clientes
- [PUT] /clientes/{cliente_id}
- [DELETE] /clientes/{cliente_id}

## Qualidade de código
```bash
black . && isort .
```

## Documentação / Swagger

- [GET] /docs
- [GET] /redoc

