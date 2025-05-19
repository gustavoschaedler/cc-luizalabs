from unittest.mock import patch

from apiluizalabs.services.product_service import ProductService


class TestProductService:
    def test_get_all_products(self, monkeypatch):
        """Testa obtenção de todos os produtos"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "mock")
        service = ProductService()
        # Adiciona alguns produtos de teste
        service.create_mock_products(3)
        produtos = service.get_all_products()
        assert len(produtos) >= 3
        assert isinstance(produtos, list)

    def test_get_product(self, monkeypatch):
        """Testa obtenção de produto específico"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "mock")
        service = ProductService()
        # Adiciona produto de teste
        produtos = service.create_mock_products(1)
        produto_id = produtos[0]["id"]
        produto = service.get_product(produto_id)
        assert produto["id"] == produto_id

    def test_product_exists(self, monkeypatch):
        """Testa verificação de existência de produto"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "mock")
        service = ProductService()
        # Adiciona produto de teste
        produtos = service.create_mock_products(1)
        produto_id = produtos[0]["id"]
        assert service.product_exists(produto_id) is True
        assert service.product_exists("produto-inexistente") is False

    @patch("requests.get")
    def test_api_service_get_all_error(self, mock_get, monkeypatch):
        """Testa erro na obtenção de produtos via API"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "api")
        monkeypatch.setenv("PRODUCTS_API_URL", "http://exemplo.com/api")
        mock_get.side_effect = Exception("Erro de conexão")
        service = ProductService()

        # Verificar se o erro é tratado
        produtos = service.get_all_products()
        assert produtos is None

    @patch("requests.get")
    def test_api_service_get_error(self, mock_get, monkeypatch):
        """Testa erro na obtenção de produto específico via API"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "api")
        monkeypatch.setenv("PRODUCTS_API_URL", "http://exemplo.com/api")
        mock_get.side_effect = Exception("Erro de conexão")
        service = ProductService()

        # Verificar se o erro é tratado
        produto = service.get_product("produto-1")
        assert produto is None

    @patch("requests.get")
    def test_api_service_exists_error(self, mock_get, monkeypatch):
        """Testa erro na verificação de existência de produto via API"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "api")
        monkeypatch.setenv("PRODUCTS_API_URL", "http://exemplo.com/api")
        mock_get.side_effect = Exception("Erro de conexão")
        service = ProductService()

        # Verificar se o erro é tratado
        result = service.product_exists("produto-1")
        assert result is False
