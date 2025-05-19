from apiluizalabs.repositories.client_repository import ClientRepository
from apiluizalabs.repositories.favorite_repository import FavoriteRepository
from apiluizalabs.services.product_service import ProductService


class FavoriteService:
    def __init__(self):
        self.repository = FavoriteRepository()
        self.client_repository = ClientRepository()
        self.product_service = ProductService()

    def get_favorites(self, email):
        """Retorna os produtos favoritos de um cliente"""
        # Verificar se o cliente existe
        client = self.client_repository.get_by_email(email)
        if not client:
            return None

        favorites = self.repository.get_favorites(email)
        # Garantir que sempre retorne uma lista, mesmo que vazia
        if favorites is None:
            favorites = []

        return favorites

    def add_favorite(self, email, product_id):
        """Adiciona um produto aos favoritos do cliente"""
        # Verificar se o cliente existe
        client = self.client_repository.get_by_email(email)
        if not client:
            return None

        # Verificar se o produto existe
        product = self.product_service.get_product(product_id)
        if not product:
            return None

        result = self.repository.add_favorite(email, product)
        # Garantir que sempre retorne uma lista, mesmo que vazia
        if result is None:
            result = []

        return result

    def remove_favorite(self, email, product_id):
        """Remove um produto dos favoritos do cliente"""
        # Verificar se o cliente existe
        client = self.client_repository.get_by_email(email)
        if not client:
            return None

        result = self.repository.remove_favorite(email, product_id)
        if result is None:
            return None

        return result
