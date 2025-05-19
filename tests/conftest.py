import pytest
from fastapi.testclient import TestClient

from apiluizalabs.main import app
from apiluizalabs.models import mem_clients, mem_products


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth():
    # Ao inves de retornar as credenciais, vai retornar um token valido p/ ser usado nos tetes
    from datetime import timedelta

    from apiluizalabs.auth import create_access_token

    access_token = create_access_token(
        data={"sub": "admin"}, expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(autouse=True)
def setup_test_data():
    """Fixture para limpar o estado e configurar dados de teste antes de cada execucao de teste"""
    # Limpa o estado dos clientes e produtos
    mem_clients.clear()
    mem_products.clear()

    # Adiciona produtos mock basicos para os testes (2 para testes de favoritos)
    mem_products["prod-000001"] = {
        "id": "prod-000001",
        "title": "Mock Product 1",
        "price": 10.0,
        "image": "img1.jpg",
        "brand": "Brand1",
        "reviewScore": 4.5,
    }
    mem_products["prod-000002"] = {
        "id": "prod-000002",
        "title": "Mock Product 2",
        "price": 20.0,
        "image": "img2.jpg",
        "brand": "Brand2",
        "reviewScore": 4.0,
    }

    # Retorna o controle para o teste (via yield)
    yield

    # Clean apos os testes
    mem_clients.clear()
    mem_products.clear()
