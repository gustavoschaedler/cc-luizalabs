import pytest

from apiluizalabs.models import mem_products
from apiluizalabs.services.client_service import ClientService
from apiluizalabs.services.favorite_service import FavoriteService


class TestFavorites:
    def test_add_favorite(self, client, auth):
        # Criar cliente para teste
        client.post(
            "/clients/",
            json={"name": "Maria", "email": "maria@email.com"},
            headers=auth,
        )

        # Garantir que o produto existe
        product_id = "PROD-ADDFAV"
        mem_products[product_id] = {
            "id": product_id,
            "title": "Produto para Favoritar",
            "price": 99.9,
            "image": "fav.jpg",
            "brand": "FavBrand",
            "reviewScore": 4.5,
        }

        # Adicionar aos favoritos
        resp = client.post(
            f"/favorites/maria@email.com",
            json={"id": product_id},
            headers=auth,
        )

        assert resp.status_code == 200
        data = resp.json()
        assert "favorites" in data
        assert isinstance(data["favorites"], list)
        assert len(data["favorites"]) == 1
        assert data["favorites"][0]["id"] == product_id

    def test_add_favorite_client_not_found(self, client, auth):
        resp = client.post(
            "/favorites/naoexiste@email.com",
            json={"id": "PROD-001"},
            headers=auth,
        )
        assert resp.status_code == 404
        assert "Cliente ou produto nao encontrado" in resp.json()["detail"]

    def test_get_favorites(self, client, auth):
        # Cria cliente e produto
        client.post(
            "/clients/",
            json={"name": "Fav Test", "email": "favtest@email.com"},
            headers=auth,
        )

        if "prod-000001" not in mem_products:
            mem_products["prod-000001"] = {
                "id": "prod-000001",
                "title": "Mock Product 1",
                "price": 10.0,
                "image": "img1.jpg",
                "brand": "Brand1",
                "reviewScore": 4.5,
            }

        # Adiciona favorito diretamente via serviço
        favorite_service = FavoriteService()
        favorite_service.add_favorite("favtest@email.com", "prod-000001")

        # Obtém favoritos
        resp = client.get("/favorites/favtest@email.com", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert "favorites" in data
        assert isinstance(data["favorites"], list)
        assert len(data["favorites"]) == 1
        assert data["favorites"][0]["id"] == "prod-000001"

    def test_get_favorites_client_exists_no_favorites(self, client, auth):
        # Cria cliente sem favoritos
        client.post(
            "/clients/",
            json={"name": "SemFavoritos", "email": "semfav@email.com"},
            headers=auth,
        )

        # Verifica que retorna lista vazia
        resp = client.get("/favorites/semfav@email.com", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert "favorites" in data
        assert isinstance(data["favorites"], list)
        assert len(data["favorites"]) == 0

    def test_get_favorites_client_not_found(self, client, auth):
        resp = client.get("/favorites/naoexiste@email.com", headers=auth)
        assert resp.status_code == 404
        assert "Cliente nao encontrado" in resp.json()["detail"]

    def test_remove_favorite(self, client, auth):
        # Cria cliente e produto
        client.post(
            "/clients/",
            json={"name": "Remove Test", "email": "removetest@email.com"},
            headers=auth,
        )

        product_id = "PROD-REMOVE"
        mem_products[product_id] = {
            "id": product_id,
            "title": "Produto para Remover",
            "price": 50.0,
            "image": "remove.jpg",
            "brand": "RemoveBrand",
            "reviewScore": 3.5,
        }

        # Adiciona favorito
        client_service = ClientService()
        favorite_service = FavoriteService()
        favorite_service.add_favorite("removetest@email.com", product_id)

        # Remove favorito
        resp = client.delete(
            f"/favorites/removetest@email.com/{product_id}", headers=auth
        )

        assert resp.status_code == 200
        data = resp.json()
        assert "favorites" in data
        assert isinstance(data["favorites"], list)
        assert len(data["favorites"]) == 0

    def test_remove_favorite_not_found(self, client, auth):
        # Cria cliente sem favoritos
        client.post(
            "/clients/",
            json={"name": "Sem Fav", "email": "semfav2@email.com"},
            headers=auth,
        )

        # Tenta remover favorito inexistente
        resp = client.delete(
            "/favorites/semfav2@email.com/produto-inexistente", headers=auth
        )

        assert resp.status_code == 404
        assert "Produto nao esta nos favoritos" in resp.json()["detail"]
