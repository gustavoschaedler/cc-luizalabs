import os
from unittest.mock import MagicMock, patch

import pytest

from apiluizalabs.models import mem_products
from apiluizalabs.repositories.product_repository import ProductRepository
from apiluizalabs.services.product_service import ProductService


class TestProducts:
    def test_list_products_success_mock(self, client, auth):
        if os.getenv("PRODUCTS_SOURCE", "api") == "mock":
            resp = client.get("/products/", headers=auth)
            assert resp.status_code == 200
            data = resp.json()
            assert isinstance(data, dict)
            assert "results" in data
            assert isinstance(data["results"], list)
            assert data["total"] >= 2

    def test_get_product_mock(self, client, auth):
        if os.getenv("PRODUCTS_SOURCE", "api") == "mock":
            product_id = "PROD-MOCKGET"
            mem_products[product_id] = {
                "id": product_id,
                "title": "Test Get Mock",
                "price": 1.0,
                "image": "get.jpg",
                "brand": "Get",
                "reviewScore": 3.0,
            }
            resp = client.get(f"/products/{product_id}", headers=auth)
            assert resp.status_code == 200
            assert resp.json()["id"] == product_id

    @pytest.mark.parametrize("source", ["api", "mock"])
    def test_product_service_factory(self, source):
        with patch("os.getenv", return_value=source):
            service = ProductService()
            if source == "api":
                assert service.repository.source == "api"
            else:
                assert service.repository.source == "mock"

    @patch("apiluizalabs.repositories.product_repository.httpx.get")
    def test_product_api_service_get_all_success(self, mock_httpx_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "api-1"}, {"id": "api-2"}]
        mock_httpx_get.return_value = mock_response

        repository = ProductRepository(
            source="api", api_url="http://fakeapi.com/products"
        )
        result = repository.get_all()
        mock_httpx_get.assert_called_once_with(
            "http://fakeapi.com/products",
            headers={"Authorization": f"Bearer {os.getenv('PRODUCTS_API_AUTHORIZATION')}"}
        )
        assert len(result) == 2
        assert result[0]["id"] == "api-1"

    @patch("apiluizalabs.repositories.product_repository.httpx.get")
    def test_product_api_service_get_all_error(self, mock_httpx_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_httpx_get.return_value = mock_response

        repository = ProductRepository(
            source="api", api_url="http://fakeapi.com/products"
        )
        result = repository.get_all()
        mock_httpx_get.assert_called_once_with(
            "http://fakeapi.com/products",
            headers={"Authorization": f"Bearer {os.getenv('PRODUCTS_API_AUTHORIZATION')}"}
        )
        assert result == []

    @patch("apiluizalabs.repositories.product_repository.httpx.get")
    def test_product_api_service_get_one_success(self, mock_httpx_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "api-1", "name": "API Product 1"}
        mock_httpx_get.return_value = mock_response

        repository = ProductRepository(
            source="api", api_url="http://fakeapi.com/products"
        )
        result = repository.get_by_id("api-1")
        mock_httpx_get.assert_called_once_with(
            "http://fakeapi.com/products/api-1",
            headers={"Authorization": f"Bearer {os.getenv('PRODUCTS_API_AUTHORIZATION')}"}
        )
        assert result == {"id": "api-1", "name": "API Product 1"}


# Também precisamos importar a função get_product_service
from apiluizalabs.services.product_service import ProductService


def get_product_service():
    return ProductService()


def test_list_products_empty(client, auth, monkeypatch):
    """Testa listagem quando nao existe produtos"""
    # Substituir diretamente a funcao na rota
    original_get_all = get_product_service().get_all_products

    def mock_get_all():
        return []

    # Substituir o método get_all no modulo de rotas
    monkeypatch.setattr(
        "apiluizalabs.routes.products.product_service.get_all_products", mock_get_all
    )

    try:
        resp = client.get("/products/", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["results"] == []
    finally:
        # Restaurar o metodo original
        monkeypatch.setattr(
            "apiluizalabs.routes.products.product_service.get_all_products",
            original_get_all,
        )


def test_list_products_error(client, auth, monkeypatch):
    """Testa erro ao acessar produtos"""
    # Substitui diretamente a funcao na rota
    original_get_all = get_product_service().get_all_products

    def mock_get_all():
        return None

    # Substitui o metodo get_all no modulo dee rotas
    monkeypatch.setattr(
        "apiluizalabs.routes.products.product_service.get_all_products", mock_get_all
    )

    try:
        resp = client.get("/products/", headers=auth)
        assert resp.status_code == 502
        assert "Erro ao acessar produtos" in resp.json()["detail"]
    finally:
        # Restaurar o metodo original
        monkeypatch.setattr(
            "apiluizalabs.routes.products.product_service.get_all_products",
            original_get_all,
        )


def test_create_mock_products_error(client, auth, monkeypatch):
    """Testa erro ao criar produtos mockados"""
    # Substitui diretamente a funcao na rota
    original_create_mock = get_product_service().create_mock_products

    def mock_create_mock_products(*args, **kwargs):
        raise ValueError("Erro ao criar produtos")

    # Substitui o metodo no modulos de rotas
    monkeypatch.setattr(
        "apiluizalabs.routes.products.product_service.create_mock_products",
        mock_create_mock_products,
    )

    try:
        resp = client.post("/products/mock/5", headers=auth)
        assert resp.status_code == 400
        assert "Erro ao criar produtos" in resp.json()["detail"]
    finally:
        # Restaura o metodo original se possiivel
        if hasattr(get_product_service(), "create_mock_products"):
            monkeypatch.setattr(
                "apiluizalabs.routes.products.product_service.create_mock_products",
                original_create_mock,
            )


def test_get_product_not_found(client, auth):
    """Testa obtenção de produto inexistente"""
    resp = client.get("/products/produto-inexistente", headers=auth)
    assert resp.status_code == 404
    assert "Not Found" in resp.json()["detail"]
