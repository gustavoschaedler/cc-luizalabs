import pytest
from fastapi import HTTPException
from jose import jwt

from apiluizalabs.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
)


class TestAuth:
    def test_authenticate_user_success(self):
        """Teste de autenticacao sucesso"""
        user = authenticate_user("admin", "admin123")
        assert user is not None
        assert user["username"] == "admin"

    def test_authenticate_user_invalid_credentials(self):
        """Teste de autenticacao com credenciais invalidas"""
        user = authenticate_user("admin", "senha_errada")
        assert user is False

    def test_authenticate_user_invalid_username(self):
        """Testa autenticacao com usuário inválido"""
        result = authenticate_user("usuario_inexistente", "senha_qualquer")
        assert result is False

    def test_authenticate_user_invalid_password(self):
        """Testa autenticacao com senha invalida"""
        result = authenticate_user("admin", "senha_incorreta")
        assert result is False

    def test_create_access_token_with_expiration(self):
        """Testa criação de token com expiração personalizada"""
        from datetime import timedelta

        token = create_access_token(
            data={"sub": "test_user"}, expires_delta=timedelta(minutes=30)
        )
        assert token is not None
        assert isinstance(token, str)

    def test_get_current_user_invalid_payload(self):
        """Testa obtenção de usuário com payload invalido"""
        # Cria token com payload invalido por exmeplo (sem 'sub')
        token = jwt.encode({"data": "invalid"}, SECRET_KEY, algorithm=ALGORITHM)

        with pytest.raises(HTTPException) as excinfo:
            get_current_user(token)

        assert excinfo.value.status_code == 401
        assert "Não autorizado" in excinfo.value.detail

    def test_login_endpoint_success(self, client):
        """Teste de endpoint de login com credenciais validas"""
        response = client.post(
            "/token",
            data={"username": "admin", "password": "admin123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_endpoint_invalid_credentials(self, client):
        """Teste de endpoint de login com credenciais invalidas"""
        response = client.post(
            "/token",
            data={"username": "admin", "password": "senha_errada"},
        )
        assert response.status_code == 400
        assert "Usuário ou senha incorretos" in response.json()["detail"]

    def test_protected_endpoint_with_valid_token(self, client):
        """Teste de acesso a endpoint protegido com token valido"""
        # Primeiro, obter um token valido
        login_response = client.post(
            "/token",
            data={"username": "admin", "password": "admin123"},
        )
        token = login_response.json()["access_token"]

        # Usar o token para acessar um endpoint protegido
        response = client.get("/clients/", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200

    def test_protected_endpoint_without_token(self, client):
        """Teste de acesso a endpoint protegido sem token"""
        response = client.get("/clients/")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
