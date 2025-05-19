from app.models import mem_products


class TestFavorites:
    def test_add_favorite(self, client, auth):
        client.post(
            "/clients/",
            json={"name": "Maria", "email": "maria@email.com"},
            headers=auth,
        )

        resp = client.post(
            "/favorites/maria@email.com",
            json={"product_id": "prod-000001"},
            headers=auth,
        )
        assert resp.status_code == 201

    def test_get_favorites(self, client, auth):
        # Cria cliente e produto
        client.post(
            "/clients/",
            json={"name": "Fav Test", "email": "favtest@email.com", "favorites": []},
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
        # Adiciona favorito
        client.patch(
            "/clients/favtest@email.com",
            json={"favorites": ["prod-000001"]},
            headers=auth,
        )
        resp = client.get("/favorites/favtest@email.com", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "results" in data
        assert isinstance(data["results"], list)
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == "prod-000001"

    def test_get_favorites_client_exists_no_favorites(self, client, auth):
        client.post(
            "/clients/",
            json={"name": "SemFavoritos", "email": "semfav@email.com"},
            headers=auth,
        )
        resp = client.get("/favorites/semfav@email.com", headers=auth)
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Nenhum produto favorito foi encontrado"

    def test_remove_favorite(self, client, auth):
        client.post(
            "/clients/",
            json={"name": "Maria", "email": "maria@email.com"},
            headers=auth,
        )
        client.post(
            "/favorites/maria@email.com",
            json={"product_id": "prod-000001"},
            headers=auth,
        )

        resp_delete = client.delete(
            "/favorites/maria@email.com/prod-000001", headers=auth
        )
        assert resp_delete.status_code == 200
        assert resp_delete.json()["msg"] == "Produto removido dos favoritos com sucesso"

        resp_get = client.get("/favorites/maria@email.com", headers=auth)
        assert resp_get.status_code == 404
        assert resp_get.json()["detail"] == "Nenhum produto favorito foi encontrado"

    def test_duplicate_favorite(self, client, auth):
        client.post(
            "/clients/",
            json={"name": "Cliente Teste Fav", "email": "teste_fav_dup@email.com"},
            headers=auth,
        )
        if "prod-000002" not in mem_products:
            mem_products["prod-000002"] = {
                "id": "prod-000002",
                "title": "Mock Product 2",
                "price": 20.0,
                "image": "img2.jpg",
                "brand": "Brand2",
                "reviewScore": 4.0,
            }

        client.post(  # Adiciona primeira vez
            "/favorites/teste_fav_dup@email.com",
            json={"product_id": "prod-000002"},
            headers=auth,
        )

        resp = client.post(  # Tenta adicionar de novo
            "/favorites/teste_fav_dup@email.com",
            json={"product_id": "prod-000002"},
            headers=auth,
        )
        assert resp.status_code == 400
        assert resp.json()["detail"] == "Produto ja favoritado"


    def test_get_favorites_client_not_found(self, client, auth):
        """Testa obtenção de favoritos para cliente inexistente"""
        resp = client.get("/favorites/cliente_inexistente@email.com", headers=auth)
        assert resp.status_code == 404
        assert "Cliente nao encontrado" in resp.json()["detail"]
    
    def test_add_favorite_client_not_found(self, client, auth):
        """Testa adição de favorito para cliente inexistente"""
        resp = client.post(
            "/favorites/cliente_inexistente@email.com",
            json={"product_id": "prod-000001"},
            headers=auth
        )
        assert resp.status_code == 404
        assert "Cliente nao encontrado" in resp.json()["detail"]
    
    def test_add_favorite_product_not_found(self, client, auth):
        """Testa adição de produto inexistente aos favoritos"""
        # Cria cliente para teste
        client.post(
            "/clients/",
            json={"name": "Cliente Teste", "email": "cliente_teste_fav@email.com"},
            headers=auth
        )
        
        resp = client.post(
            "/favorites/cliente_teste_fav@email.com",
            json={"product_id": "produto-inexistente"},
            headers=auth
        )
        assert resp.status_code == 404
        assert "Produto nao encontrado" in resp.json()["detail"]
    
    def test_remove_favorite_client_not_found(self, client, auth):
        """Testa remoção de favorito para cliente inexistente"""
        resp = client.delete(
            "/favorites/cliente_inexistente@email.com/prod-000001",
            headers=auth
        )
        assert resp.status_code == 404
        assert "Cliente nao encontrado" in resp.json()["detail"]
    
    def test_remove_favorite_product_not_found(self, client, auth):
        """Testa remoção de produto inexistente dos favoritos"""
        # Cria cliente para teste
        client.post(
            "/clients/",
            json={"name": "Cliente Teste", "email": "cliente_teste_rem@email.com"},
            headers=auth
        )
        
        resp = client.delete(
            "/favorites/cliente_teste_rem@email.com/produto-inexistente",
            headers=auth
        )
        assert resp.status_code == 404
        # Corrigir a mensagem esperada para corresponder à real
        assert "Produto nao esta nos favoritos" in resp.json()["detail"]
