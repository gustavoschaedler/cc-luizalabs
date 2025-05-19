from apiluizalabs.models import mem_clients


class FavoriteRepository:
    def get_favorites(self, email):
        """Retorna os produtos favoritos de um cliente"""
        client = mem_clients.get(email)
        if not client:
            return None

        if "favorites" not in client:
            client["favorites"] = []

        return client.get("favorites", [])

    def add_favorite(self, email, product):
        """Adiciona um produto aos favoritos do cliente"""
        client = mem_clients.get(email)
        if not client:
            return None

        if "favorites" not in client:
            client["favorites"] = []

        for fav in client["favorites"]:
            if fav["id"] == product["id"]:
                return client["favorites"]

        client["favorites"].append(product)
        return client["favorites"]

    def remove_favorite(self, email, product_id):
        """Remove um produto dos favoritos do cliente"""
        client = mem_clients.get(email)
        if not client:
            return None

        if "favorites" not in client:
            client["favorites"] = []
            return client["favorites"]

        # Verifica se o produto esta nos favoritos
        for i, fav in enumerate(client["favorites"]):
            if fav["id"] == product_id:
                client["favorites"].pop(i)
                return client["favorites"]

        return None  # Prod nao encontrado
