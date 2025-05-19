from apiluizalabs.repositories.client_repository import ClientRepository
from apiluizalabs.services.product_service import ProductService


class ClientService:
    def __init__(self):
        self.repository = ClientRepository()
        self.product_service = ProductService()

    def get_all_clients(self):
        """Retorna todos os clientes"""
        clients = self.repository.get_all()
        return {"total": len(clients), "page": 1, "results": clients}

    def get_client(self, email):
        """Retorna um cliente pelo email"""
        return self.repository.get_by_email(email)

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
        return self.repository.create(client_data)

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
        return self.repository.update(email, client_data)

    def delete_client(self, email):
        """Remove um cliente pelo email"""
        client = self.repository.delete(email)
        if client:
            return {"detail": "Cliente removido com sucesso"}
        return None
