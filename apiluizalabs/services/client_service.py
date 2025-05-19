from apiluizalabs.repositories.client_repository import ClientRepository
from apiluizalabs.services.product_service import ProductService
from apiluizalabs.utils.cache import LRUCacheTTL


class ClientService:
    def __init__(self):
        self.repository = ClientRepository()
        self.product_service = ProductService()
        # Inicializado o cache com capacidade para 512 clientes e TTL de 30 segundos
        self.cache = LRUCacheTTL(capacity=512, ttl=30)

    def get_all_clients(self):
        """Retorna todos os clientes"""
        clients = self.repository.get_all()
        return {"total": len(clients), "page": 1, "results": clients}

    def get_client(self, email):
        """Retorna um cliente pelo email"""
        # Tenta obter do cache primeiro
        cached_client = self.cache.get(email)
        if cached_client:
            return cached_client

        # Se não estiver no cache, busca no repositório
        client = self.repository.get_by_email(email)

        # Se encontrou, armazena no cache
        if client:
            self.cache.put(email, client)

        return client

    def create_client(self, client_data):
        """Cria um novo cliente"""
        # Verificar se o cliente ja existente
        email = client_data.get("email")
        if self.repository.email_exists(email):
            return {"error": "Email existente, forneca outro email"}

        # Verificar se ha produtos favoritos na requisicao
        favorites = client_data.get("favorites", [])
        if favorites:
            # Verificar se aá produtos duplicados
            if len(favorites) != len(set(favorites)):
                duplicates = [item for item in favorites if favorites.count(item) > 1]
                return {"error": f"Produtos duplicados: {', '.join(duplicates)}"}

            # Verificar se todos os produtos existem
            non_existent = []
            for product_id in favorites:
                if not self.product_service.product_exists(product_id):
                    non_existent.append(product_id)

            if non_existent:
                return {"error": f"Produtos nao encontrado: {', '.join(non_existent)}"}

            # Substituir IDs por objetos de produto
            product_objects = []
            for product_id in favorites:
                product = self.product_service.get_product(product_id)
                if product:
                    product_objects.append(product)

            client_data["favorites"] = product_objects
        else:
            client_data["favorites"] = []

        # Criar o cliente
        client = self.repository.create(client_data)

        # Adiciona ao cache
        self.cache.put(email, client)

        return client

    def update_client(self, email, client_data):
        """Atualiza um cliente existente"""
        # Verificar se o cliente existe
        if not self.repository.get_by_email(email):
            return None

        # Verificar se esta tentando atualizar p/ um email que ja existe
        new_email = client_data.get("email")
        if new_email and new_email != email and self.repository.email_exists(new_email):
            return {"error": "Email existente, forneca outro email"}

        # Verificar se há produtos favoritos na requisicao
        favorites = client_data.get("favorites")
        if favorites is not None:
            # Verificar se há produtos duplicados
            if len(favorites) != len(set(favorites)):
                duplicates = [item for item in favorites if favorites.count(item) > 1]
                return {"error": f"Produtos duplicados: {', '.join(duplicates)}"}

            # Verificar se todos os produtos existem
            non_existent = []
            for product_id in favorites:
                if not self.product_service.product_exists(product_id):
                    non_existent.append(product_id)

            if non_existent:
                return {"error": f"Produtos nao encontrado: {', '.join(non_existent)}"}

            # Substituir IDs por objetos de produto
            product_objects = []
            for product_id in favorites:
                product = self.product_service.get_product(product_id)
                if product:
                    product_objects.append(product)

            client_data["favorites"] = product_objects

        # Atualizar o cliente
        updated_client = self.repository.update(email, client_data)

        # Invalidar cache do email antigo
        self.cache.invalidate(email)

        # Se o email foi alterado, adicionar ao cache com o novo email
        if updated_client and new_email and new_email != email:
            self.cache.put(new_email, updated_client)
        # Caso contrário, atualizar o cache com o email atual
        elif updated_client:
            self.cache.put(email, updated_client)

        return updated_client

    def delete_client(self, email):
        """Remove um cliente pelo email"""
        client = self.repository.delete(email)
        if client:
            # Invalidar cache
            self.cache.invalidate(email)
            return {"detail": "Cliente removido com sucesso"}
        return None
