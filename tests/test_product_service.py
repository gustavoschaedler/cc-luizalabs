import pytest
from unittest.mock import patch, MagicMock
from app.services.product_service import get_product_service
import os

class TestProductService:
    def test_mock_service_get_all(self, monkeypatch):
        """Testa obtenção de todos os produtos no serviço mock"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "mock")
        service = get_product_service()
        # Adiciona alguns produtos de teste
        service.create_mock_products(3)
        produtos = service.get_all()
        assert len(produtos) >= 3
        assert isinstance(produtos, list)
    
    def test_mock_service_get(self, monkeypatch):
        """Testa obtenção de produto específico no serviço mock"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "mock")
        service = get_product_service()
        # Adiciona produto de teste
        produtos = service.create_mock_products(1)
        produto_id = produtos[0]["id"]
        produto = service.get(produto_id)
        assert produto["id"] == produto_id
    
    def test_mock_service_exists(self, monkeypatch):
        """Testa verificação de existência de produto no serviço mock"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "mock")
        service = get_product_service()
        # Adiciona produto de teste
        produtos = service.create_mock_products(1)
        produto_id = produtos[0]["id"]
        assert service.exists(produto_id) is True
        assert service.exists("produto-inexistente") is False
    
    @patch('requests.get')
    def test_api_service_get_all_error(self, mock_get, monkeypatch):
        """Testa erro na obtenção de produtos via API"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "api")
        monkeypatch.setenv("PRODUCTS_API_URL", "http://exemplo.com/api")
        mock_get.side_effect = Exception("Erro de conexão")
        service = get_product_service()
        
        # Verificar se a exceção é lançada
        with pytest.raises(Exception):
            service.get_all()
    
    @patch('requests.get')
    def test_api_service_get_error(self, mock_get, monkeypatch):
        """Testa erro na obtenção de produto específico via API"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "api")
        monkeypatch.setenv("PRODUCTS_API_URL", "http://exemplo.com/api")
        mock_get.side_effect = Exception("Erro de conexão")
        service = get_product_service()
        
        # Verificar se a exceção é lançada
        with pytest.raises(Exception):
            service.get("produto-1")
    
    @patch('requests.get')
    def test_api_service_exists_error(self, mock_get, monkeypatch):
        """Testa erro na verificação de existência de produto via API"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "api")
        monkeypatch.setenv("PRODUCTS_API_URL", "http://exemplo.com/api")
        mock_get.side_effect = Exception("Erro de conexão")
        service = get_product_service()
        
        # Verificar se a exceção é lançada
        with pytest.raises(Exception):
            service.exists("produto-1")
    
    def test_get_product_service_mock(self, monkeypatch):
        """Testa factory de serviço com fonte mock"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "mock")
        service = get_product_service()
        assert hasattr(service, 'create_mock_products')
    
    def test_get_product_service_api(self, monkeypatch):
        """Testa factory de serviço com fonte API"""
        monkeypatch.setenv("PRODUCTS_SOURCE", "api")
        monkeypatch.setenv("PRODUCTS_API_URL", "http://exemplo.com/api")
        service = get_product_service()
        assert not hasattr(service, 'create_mock_products')