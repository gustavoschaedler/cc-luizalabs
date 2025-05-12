from fastapi import FastAPI
from app.routes import clients, favorites, products
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)


PRODUCTS_SOURCE = os.getenv("PRODUCTS_SOURCE", "api")
PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL", None)


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
if PRODUCTS_SOURCE == "mock":
    app.include_router(products.router)


@app.get("/", tags=["Base"])
def read_root():
    return {
        "message": "API de Produtos Favoritos - Swagger e ReDoc",
        "docs": "/docs",
        "redoc": "/redoc",
    }

@app.get("/envs", tags=["Base"])
def list_envs():
    import os
    return dict(os.environ)
