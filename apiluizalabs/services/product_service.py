import os

from apiluizalabs.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        source = os.getenv("PRODUCTS_SOURCE", "api")
        api_url = os.getenv("PRODUCTS_API_URL")
        self.repository = ProductRepository(source=source, api_url=api_url)

    def get_all_products(self):
        """Retorna todos os produtos"""
        try:
            return self.repository.get_all()
        except Exception as e:
            # Log do erro
            print(f"Erro ao obter produtos: {str(e)}")
            return None

    def get_product(self, product_id):
        """Retorna um produto pelo ID"""
        try:
            return self.repository.get_by_id(product_id)
        except Exception as e:
            # Log do erro
            print(f"Erro ao obter produto {product_id}: {str(e)}")
            return None

    def product_exists(self, product_id):
        """Verifica se um produto existe"""
        try:
            return self.repository.exists(product_id)
        except Exception as e:
            # Log do erro
            print(f"Erro ao verificar produto {product_id}: {str(e)}")
            return False

    def create_mock_products(self, total):
        """Cria produtos mockados (apenas para testes)"""
        try:
            return self.repository.create_mock_products(total)
        except Exception as e:
            # Log do erro
            print(f"Erro ao criar produtos mockados: {str(e)}")
            raise e
