import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm

from apiluizalabs.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)
from apiluizalabs.routes import clients, favorites, products

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)


PRODUCTS_SOURCE = os.getenv("PRODUCTS_SOURCE", "api")
PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL", None)
PRODUCTS_API_AUTHORIZATION = os.getenv("PRODUCTS_API_AUTHORIZATION", None)


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
    docs_url=None,
    redoc_url="/redoc",
)


app.include_router(clients.router)
app.include_router(favorites.router)
if PRODUCTS_SOURCE == "mock":
    app.include_router(products.router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "API de Produtos Favoritos - Swagger e ReDoc",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/envs", tags=["Debug"])
def list_envs():
    import os

    return dict(os.environ)


@app.get("/healthcheck", tags=["DevOps"])
def healthcheck():
    return {"status": "ok"}


@app.post("/token", tags=["Autenticacao"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Configuracao personalizada do Swagger UI para suportar o token de autenticacao
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Documentação",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
        },
    )


# Personalizacao do esquema OpenAPI para incluir configuracao de seguranca
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Adiciona configuracao de seguranca para o token JWT
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Insira o token JWT obtido na rota /token",
        }
    }

    # Aplica a segurança globalmente para todas as rotas
    openapi_schema["security"] = [{"bearerAuth": []}]

    return openapi_schema
