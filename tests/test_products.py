import os
from unittest.mock import MagicMock, patch

import pytest

from app.models import mem_products
from app.services.product_service import ProductAPIService, ProductMockService, get_product_service


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
            from app.services.product_service import get_product_service

            service = get_product_service()
            if source == "api":
                assert isinstance(service, ProductAPIService)
            else:
                assert isinstance(service, ProductMockService)

    @patch("app.services.product_service.requests.get")
    def test_product_api_service_get_all_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "api-1"}, {"id": "api-2"}]
        mock_requests_get.return_value = mock_response

        service = ProductAPIService()
        with patch("os.getenv", return_value="http://fakeapi.com/products"):
            result = service.get_all()
            mock_requests_get.assert_called_once_with("http://fakeapi.com/products")
            assert len(result) == 2
            assert result[0]["id"] == "api-1"

    @patch("app.services.product_service.requests.get")
    def test_product_api_service_get_all_error(self, mock_requests_get):
        # Testa quando a API retorna erro ao buscar todos os produtos
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        service = ProductAPIService()
        with patch("os.getenv", return_value="http://fakeapi.com/products"):
            result = service.get_all()
            assert result == []

    @patch("app.services.product_service.requests.get")
    def test_product_api_service_get_one_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "api-1", "name": "API Product 1"}
        mock_requests_get.return_value = mock_response

        service = ProductAPIService()
        with patch(
            "os.getenv", return_value="http://fakeapi.com/products"
        ) as mock_os_getenv_api_url:
            result = service.get("api-1")
            # Ensure PRODUCTS_API_URL was fetched for constructing the URL
            mock_os_getenv_api_url.assert_called_with("PRODUCTS_API_URL")
            mock_requests_get.assert_called_once_with(
                "http://fakeapi.com/products/api-1"
            )
            assert result == {"id": "api-1", "name": "API Product 1"}



def test_list_products_empty(client, auth, monkeypatch):
    """Testa listagem quando não há produtos"""
    # Substituir diretamente a função na rota
    original_get_all = get_product_service().get_all
    
    def mock_get_all():
        return []
    
    # Substituir o método get_all no módulo de rotas
    monkeypatch.setattr("app.routes.products.product_service.get_all", mock_get_all)
    
    try:
        resp = client.get("/products/", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["results"] == []
    finally:
        # Restaurar o método original
        monkeypatch.setattr("app.routes.products.product_service.get_all", original_get_all)

def test_list_products_error(client, auth, monkeypatch):
    """Testa erro ao acessar produtos"""
    # Substituir diretamente a função na rota
    original_get_all = get_product_service().get_all
    
    def mock_get_all():
        return None
    
    # Substituir o método get_all no módulo de rotas
    monkeypatch.setattr("app.routes.products.product_service.get_all", mock_get_all)
    
    try:
        resp = client.get("/products/", headers=auth)
        assert resp.status_code == 502
        assert "Erro ao acessar produtos" in resp.json()["detail"]
    finally:
        # Restaurar o método original
        monkeypatch.setattr("app.routes.products.product_service.get_all", original_get_all)

def test_create_mock_products_error(client, auth, monkeypatch):
    """Testa erro ao criar produtos mockados"""
    # Substituir diretamente a função na rota
    original_create_mock = get_product_service().create_mock_products
    
    def mock_create_mock_products(*args, **kwargs):
        raise ValueError("Erro ao criar produtos")
    
    # Substituir o método no módulo de rotas
    monkeypatch.setattr("app.routes.products.product_service.create_mock_products", 
                        mock_create_mock_products)
    
    try:
        resp = client.post("/products/mock/5", headers=auth)
        assert resp.status_code == 400
        assert "Erro ao criar produtos" in resp.json()["detail"]
    finally:
        # Restaurar o método original se possível
        if hasattr(get_product_service(), "create_mock_products"):
            monkeypatch.setattr("app.routes.products.product_service.create_mock_products", 
                                original_create_mock)

def test_get_product_not_found(client, auth):
    """Testa obtenção de produto inexistente"""
    resp = client.get("/products/produto-inexistente", headers=auth)
    assert resp.status_code == 404
    assert "Produto nao existe" in resp.json()["detail"]
