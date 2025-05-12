from itertools import product
from fastapi import FastAPI
from app.routes import clients, favorites, products

app = FastAPI(
    title="API de Produtos Favoritos",
    description="API para gerenciar clientes e seus produtos favoritos. Produtos sao obtidos via mock ou API LuizaLab externa.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Clientes", "description": "Operacoes relacionadas a clientes"},
        {
            "name": "Favoritos",
            "description": "Operacoes relacionadas a produtos favoritos dos clientes",
        },
    ],
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(clients.router)
app.include_router(favorites.router)
app.include_router(products.router)


@app.get("/", tags=["Base"])
def read_root():
    return {
        "message": "API de Produtos Favoritos - Swagger e ReDoc",
        "docs": "/docs",
        "redoc": "/redoc",
    }
