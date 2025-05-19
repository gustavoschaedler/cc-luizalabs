import os

import httpx

from apiluizalabs.models import mem_clients, mem_products


class FavoriteRepository:
    def get_favorites(self, email, product_source="mock"):
        """Retorna os produtos favoritos de um cliente"""

        client = mem_clients.get(email)

        if not client:
            return None

        # Verifica se a chave "favorites" existe no dicionário
        if "favorites" not in client:
            # Não modifica o dicionário, apenas retorna uma lista vazia
            return []

        # Obtém a lista de favoritos (pode ser None, lista vazia ou lista com IDs)
        favorites_ids = client["favorites"]

        # Se for None ou lista vazia, retorna lista vazia
        if not favorites_ids:
            return []

        # Se favoritos já são objetos completos, apenas retorne
        if isinstance(favorites_ids[0], dict):
            return favorites_ids

        # Se favoritos são apenas IDs, buscar os dados completos conforme a origem
        if product_source == "mock":
            return [
                mem_products[fav_id]
                for fav_id in favorites_ids
                if fav_id in mem_products
            ]
        elif product_source == "api":
            api_url = os.getenv("PRODUCTS_API_URL")
            api_auth = os.getenv("PRODUCTS_API_AUTHORIZATION")
            headers = {}

            if all([api_url, api_auth]):
                headers["Authorization"] = f"Bearer {api_auth}"
            else:
                raise Exception("API de produtos nao configurada")

            favoritos = []
            for product_id in favorites_ids:
                url = f"{api_url}/products/{product_id}"
                try:
                    resp = httpx.get(url, headers=headers)
                    if resp.status_code == 200:
                        favoritos.append(resp.json())
                except Exception:
                    continue
            return favoritos
        else:
            return []

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
