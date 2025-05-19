from apiluizalabs.models import mem_clients, mem_products
from apiluizalabs.utils.cache import LRUCacheTTL


class TestClients:
    def test_create_client(self, client, auth):
        # Verifica se eh possivel criar um cliente com nome e email validos
        resp = client.post(
            "/clients/", json={"name": "João", "email": "joao@email.com"}, headers=auth
        )
        assert resp.status_code == 201
        assert resp.json()["email"] == "joao@email.com"
        assert "favorites" in resp.json() and resp.json()["favorites"] == []

    def test_create_client_with_initial_favorites(self, client, auth):
        # Verifica se eh possivel criar um cliente com produtos favoritos na requisicao (eh permitido)
        resp = client.post(
            "/clients/",
            json={
                "name": "Ana",
                "email": "ana@email.com",
                "favorites": ["prod-000001"],
            },
            headers=auth,
        )
        assert resp.status_code == 201
        assert resp.json()["email"] == "ana@email.com"
        assert "prod-000001" in resp.json()["favorites"]

    def test_create_client_with_non_existent_favorite(self, client, auth):
        # Verifica se eh possivel criar um cliente com produtos que nao existentem na requisicao (nao eh permitido)
        resp = client.post(
            "/clients/",
            json={
                "name": "Carlos",
                "email": "carlos@email.com",
                "favorites": ["prod-nao-existe"],
            },
            headers=auth,
        )
        assert resp.status_code == 400
        assert "Produtos nao encontrado: prod-nao-existe" in resp.json()["detail"]

    def test_create_client_with_duplicate_favorites_in_request(self, client, auth):
        # Verifica se eh possivel criar um cliente com produtos duplicados na requisicao (nao eh permitido)
        resp = client.post(
            "/clients/",
            json={
                "name": "Bia",
                "email": "bia@email.com",
                "favorites": ["prod-000001", "prod-000001"],
            },
            headers=auth,
        )
        assert resp.status_code == 400
        assert "Produtos duplicados: prod-000001" in resp.json()["detail"]

    def test_create_client_with_empty_favorites_list(self, client, auth):
        resp = client.post(
            "/clients/",
            json={"name": "Daniel", "email": "daniel@email.com", "favorites": []},
            headers=auth,
        )
        assert resp.status_code == 201
        assert resp.json()["email"] == "daniel@email.com"
        assert resp.json()["favorites"] == []

    def test_list_clients(self, client, auth):
        # Cria alguns clientes (2 para teste]
        client.post(
            "/clients/",
            json={"name": "Cliente 1", "email": "cliente1@email.com"},
            headers=auth,
        )
        client.post(
            "/clients/",
            json={"name": "Cliente 2", "email": "cliente2@email.com"},
            headers=auth,
        )
        resp = client.get("/clients/", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "results" in data
        assert isinstance(data["results"], list)
        assert len(data["results"]) >= 2
        assert data["total"] >= 2
        assert data["page"] == 1

    def test_list_clients_when_empty(self, client, auth):
        # Remove todos clientes
        for c in list(mem_clients.keys()):
            client.delete(f"/clients/{c}", headers=auth)
        resp = client.get("/clients/", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert data["results"] == []
        assert data["total"] == 0

    def test_delete_client(self, client, auth):
        # Cria um cliente novo e remove (teste da delcao)
        client.post(
            "/clients/",
            json={"name": "Cliente Del", "email": "cliente_del@email.com"},
            headers=auth,
        )
        resp = client.delete("/clients/cliente_del@email.com", headers=auth)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert data["detail"] == "Cliente removido com sucesso"
        # Check se realmente foi tudo removido com sucesso
        resp_get = client.get("/clients/cliente_del@email.com", headers=auth)
        assert resp_get.status_code == 404

    def test_update_client_all_fields_valid(self, client, auth):
        # Teste de atualizacao de cliente com todos os campos validos (eh permitido)
        client.post(
            "/clients/",
            json={
                "name": "Original",
                "email": "update_all_orig@email.com",
                "favorites": [],
            },
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

        update_data = {
            "name": "Nome Novo Completo",
            "email": "update_all_novo@email.com",
            "favorites": ["prod-000002"],
        }
        resp = client.patch(
            "/clients/update_all_orig@email.com", json=update_data, headers=auth
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Nome Novo Completo"
        assert resp.json()["email"] == "update_all_novo@email.com"
        assert "prod-000002" in resp.json()["favorites"]

    def test_update_client_favorites_add_valid(self, client, auth):
        # Teste de atualizacao de cliente com produtos favoritos adicionados (eh permitido)
        client.post(
            "/clients/",
            json={
                "name": "UpdateFavs",
                "email": "update_favs@email.com",
                "favorites": [],
            },
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

        resp = client.patch(
            "/clients/update_favs@email.com",
            json={"favorites": ["prod-000001"]},
            headers=auth,
        )
        assert resp.status_code == 200
        assert "prod-000001" in resp.json()["favorites"]

    def test_update_client_favorites_with_duplicate_product_in_request(
        self, client, auth
    ):
        # Teste de atualizacao de cliente com produtos favoritos duplicados na requisicao (nao eh permitido)
        client.post(
            "/clients/",
            json={"name": "UpdateFavsDup", "email": "update_favs_dup@email.com"},
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
        resp = client.patch(
            "/clients/update_favs_dup@email.com",
            json={"favorites": ["prod-000001", "prod-000001"]},
            headers=auth,
        )
        assert resp.status_code == 400
        assert "Produtos duplicados: prod-000001" in resp.json()["detail"]

    def test_create_client_with_existing_email(self, client, auth):
        # Primeiro, cria um cliente com um email específico
        client.post(
            "/clients/",
            json={"name": "Cliente Original", "email": "email_existente@email.com"},
            headers=auth,
        )

        # Tenta criar outro cliente com o mesmo email
        resp = client.post(
            "/clients/",
            json={"name": "Cliente Duplicado", "email": "email_existente@email.com"},
            headers=auth,
        )

        # Verifica se a API retorna erro 400 e a mensagem correta
        assert resp.status_code == 400
        assert "Email existente, forneca outro email" in resp.json()["detail"]

    def test_update_client_with_existing_email(self, client, auth):
        # Cria dois clientes com emails diferentes
        client.post(
            "/clients/",
            json={"name": "Cliente Um", "email": "cliente_um@email.com"},
            headers=auth,
        )
        client.post(
            "/clients/",
            json={"name": "Cliente Dois", "email": "cliente_dois@email.com"},
            headers=auth,
        )

        # Tenta atualizar o segundo cliente para usar o email do primeiro
        resp = client.patch(
            "/clients/cliente_dois@email.com",
            json={"email": "cliente_um@email.com"},
            headers=auth,
        )

        # Verifica se a API retorna erro 400 e a mensagem correta
        assert resp.status_code == 400
        assert "Email existente, forneca outro email" in resp.json()["detail"]

    def test_client_cache(self, client, auth, monkeypatch):
        """Testa se o cache está funcionando corretamente"""
        from apiluizalabs.repositories.client_repository import ClientRepository

        call_count = [0]

        original_get_by_email = ClientRepository.get_by_email

        def mock_get_by_email(self, email):
            call_count[0] += 1
            return original_get_by_email(self, email)

        monkeypatch.setattr(ClientRepository, "get_by_email", mock_get_by_email)

        client.post(
            "/clients/",
            json={"name": "Cliente Cache", "email": "cliente_cache@email.com"},
            headers=auth,
        )

        resp1 = client.get("/clients/cliente_cache@email.com", headers=auth)
        assert resp1.status_code == 200
        assert call_count[0] == 0

        resp2 = client.get("/clients/cliente_cache@email.com", headers=auth)
        assert resp2.status_code == 200
        assert call_count[0] == 0

        client.patch(
            "/clients/cliente_cache@email.com",
            json={"name": "Nome Atualizado"},
            headers=auth,
        )

        resp3 = client.get("/clients/cliente_cache@email.com", headers=auth)
        assert resp3.status_code == 200
        assert call_count[0] == 1

        resp4 = client.get("/clients/cliente_cache@email.com", headers=auth)
        assert resp4.status_code == 200
        assert call_count[0] == 1

    def test_client_cache_ttl(self, client, auth, monkeypatch):
        """Testa se o TTL do cache está funcionando corretamente"""
        import time

        from apiluizalabs.repositories.client_repository import ClientRepository
        from apiluizalabs.services.client_service import ClientService

        call_count = [0]

        original_get_by_email = ClientRepository.get_by_email

        def mock_get_by_email(self, email):
            call_count[0] += 1
            return original_get_by_email(self, email)

        monkeypatch.setattr(ClientRepository, "get_by_email", mock_get_by_email)

        service = ClientService()
        original_ttl = service.cache.ttl
        service.cache.ttl = 1.0

        client.post(
            "/clients/",
            json={"name": "Cliente TTL", "email": "cliente_ttl@email.com"},
            headers=auth,
        )

        resp1 = client.get("/clients/cliente_ttl@email.com", headers=auth)
        assert resp1.status_code == 200
        assert call_count[0] == 0

        resp2 = client.get("/clients/cliente_ttl@email.com", headers=auth)
        assert resp2.status_code == 200
        assert call_count[0] == 0

        time.sleep(1.5)

        resp3 = client.get("/clients/cliente_ttl@email.com", headers=auth)
        assert resp3.status_code == 200
        assert call_count[0] == 0

        service.cache.ttl = original_ttl
