class TestMain:
    def test_read_root(self, client):
        """Testa endpoint raiz"""
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        assert "docs" in data
        assert "redoc" in data

    def test_list_envs(self, client):
        """Testa listagem de variáveis de ambiente"""
        resp = client.get("/envs")
        assert resp.status_code == 200
        assert isinstance(resp.json(), dict)

    def test_healthcheck(self, client):
        """Testa endpoint de healthcheck"""
        resp = client.get("/healthcheck")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    def test_login_invalid_credentials(self, client):
        """Testa login com credenciais inválidas"""
        resp = client.post(
            "/token",
            data={"username": "usuario_invalido", "password": "senha_invalida"},
        )
        assert resp.status_code == 400
        assert "Usuário ou senha incorretos" in resp.json()["detail"]
