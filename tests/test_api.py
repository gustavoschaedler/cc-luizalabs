from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
auth = ("admin", "admin123")


def test_create_client():
    resp = client.post(
        "/clients/", json={"name": "João", "email": "joao@email.com"}, auth=auth
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == "joao@email.com"


def test_add_favorite():
    client.post(
        "/clients/", json={"name": "Maria", "email": "maria@email.com"}, auth=auth
    )
    resp = client.post(
        "/favorites/maria@email.com", json={"product_id": "prod-1"}, auth=auth
    )
    assert resp.status_code == 200


def test_get_favorites():
    resp = client.get("/favorites/maria@email.com", auth=auth)
    assert resp.status_code == 200
    assert resp.json()[0]["id"] == "prod-1"


def test_list_clients():
    """Testa a listagem de clientes"""
    resp = client.get("/clients/", auth=auth)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    
    emails = [c["email"] for c in resp.json()]
    assert "joao@email.com" in emails
    assert "maria@email.com" in emails


def test_remove_favorite():
    """Testa a remoção de um produto favorito"""
    resp = client.delete("/favorites/maria@email.com/prod-1", auth=auth)
    assert resp.status_code == 200
    assert resp.json()["msg"] == "Produto removido dos favoritos"

    resp = client.get("/favorites/maria@email.com", auth=auth)
    assert resp.status_code == 200
    assert len(resp.json()) == 0


def test_delete_client():
    """Testa a exclusão de um cliente"""
    client.post(
        "/clients/",
        json={"name": "Cliente Temporário", "email": "temp@email.com"},
        auth=auth,
    )

    resp = client.delete("/clients/temp@email.com", auth=auth)
    assert resp.status_code == 200
    assert resp.json()["msg"] == "Cliente removido"

    resp = client.get("/clients/", auth=auth)
    emails = [c["email"] for c in resp.json()]
    assert "temp@email.com" not in emails


def test_root_endpoint():
    """Testa o endpoint raiz da API"""
    resp = client.get("/", auth=auth)
    assert resp.status_code == 200
    assert "message" in resp.json()
    assert "docs" in resp.json()
    assert "redoc" in resp.json()


def test_authentication_required():
    """Testa se a autenticação é obrigatória"""
    resp = client.get("/clients/")
    assert resp.status_code == 401

    resp = client.get("/clients/", auth=("usuario_errado", "senha_errada"))
    assert resp.status_code == 401


def test_client_not_found():
    """Testa o comportamento quando um cliente não existe"""
    resp = client.get("/favorites/cliente_inexistente@email.com", auth=auth)
    assert resp.status_code == 404
    assert "detail" in resp.json()


def test_duplicate_client():
    """Testa a tentativa de criar um cliente com email duplicado"""
    client.post(
        "/clients/",
        json={"name": "Cliente Duplicado", "email": "duplicado@email.com"},
        auth=auth,
    )

    resp = client.post(
        "/clients/",
        json={"name": "Outro Nome", "email": "duplicado@email.com"},
        auth=auth,
    )
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_duplicate_favorite():
    """Testa a tentativa de adicionar um produto favorito duplicado"""
    client.post(
        "/clients/",
        json={"name": "Cliente Teste", "email": "teste_fav@email.com"},
        auth=auth,
    )

    client.post(
        "/favorites/teste_fav@email.com", json={"product_id": "prod-2"}, auth=auth
    )

    resp = client.post(
        "/favorites/teste_fav@email.com", json={"product_id": "prod-2"}, auth=auth
    )
    assert resp.status_code == 400
    assert "detail" in resp.json()
