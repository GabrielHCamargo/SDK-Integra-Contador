"""
Teste de persistência e carregamento de tokens.

Este teste verifica se:
1. O token é salvo corretamente em arquivo
2. O token é carregado do arquivo quando válido
3. O token é renovado quando expirado
4. A verificação de expires_in funciona corretamente
"""

import asyncio
import json
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from integra_sdk.auth.manager import AuthManager
from integra_sdk.config import Environment
from integra_sdk.types.auth import TokenResponse


@pytest.fixture
def test_certificate_path(tmp_path):
    """Fixture creating a dummy certificate file."""
    cert_file = tmp_path / "test_cert.p12"
    cert_file.write_bytes(b"dummy certificate data")
    return str(cert_file)


@pytest.fixture
def test_token_storage_path(tmp_path):
    """Fixture creating a temporary token storage directory."""
    storage_dir = tmp_path / ".auth"
    storage_dir.mkdir(parents=True, exist_ok=True)
    return str(storage_dir)


@pytest.fixture
def auth_manager_production(test_certificate_path, test_token_storage_path):
    """Fixture creating an AuthManager instance for Production."""
    return AuthManager(
        consumer_key="test_key",
        consumer_secret="test_secret",
        certificate_path=test_certificate_path,
        certificate_password="test_password",
        environment=Environment.PRODUCTION,
        token_storage_path=test_token_storage_path,
    )


@pytest.fixture
def mock_token_response_data():
    """Fixture with mock token response data."""
    return {
        "expires_in": 2000,  # 2000 seconds
        "scope": "default",
        "token_type": "Bearer",
        "access_token": "test-access-token-123",
        "jwt_token": "test-jwt-token-456",
        "jwt_pucomex": None,
    }


class TestTokenPersistence:
    """Test token persistence and loading functionality."""

    def test_save_token_to_file(
        self, auth_manager_production, mock_token_response_data, test_token_storage_path
    ):
        """Test that token is saved to file correctly."""
        token_response = TokenResponse(**mock_token_response_data)

        # Save token
        auth_manager_production._save_token_to_file(token_response)

        # Verify file exists
        token_file = Path(test_token_storage_path) / "token.json"
        assert token_file.exists(), "Token file should be created"

        # Verify file contents
        with open(token_file, "r", encoding="utf-8") as f:
            saved_data = json.load(f)

        assert saved_data["access_token"] == "test-access-token-123"
        assert saved_data["jwt_token"] == "test-jwt-token-456"
        assert saved_data["expires_in"] == 2000
        assert "saved_at" in saved_data

    def test_load_valid_token_from_file(
        self, auth_manager_production, mock_token_response_data, test_token_storage_path
    ):
        """Test loading a valid token from file."""
        token_file = Path(test_token_storage_path) / "token.json"

        # Create a token file with valid token (not expired)
        token_data = {
            **mock_token_response_data,
            "saved_at": time.time(),  # Saved now
        }
        with open(token_file, "w", encoding="utf-8") as f:
            json.dump(token_data, f)

        # Load token
        token, expires_at = auth_manager_production._load_token_from_file()

        assert token is not None, "Token should be loaded"
        assert token.access_token == "test-access-token-123"
        assert expires_at is not None
        assert expires_at > time.time(), "Token should not be expired"

    def test_load_expired_token_from_file(
        self, auth_manager_production, test_token_storage_path
    ):
        """Test loading an expired token from file."""
        token_file = Path(test_token_storage_path) / "token.json"

        # Create a token file with expired token
        token_data = {
            "expires_in": 100,  # 100 seconds
            "scope": "default",
            "token_type": "Bearer",
            "access_token": "expired-token",
            "jwt_token": "expired-jwt",
            "jwt_pucomex": None,
            "saved_at": time.time() - 200,  # Saved 200 seconds ago (expired)
        }
        with open(token_file, "w", encoding="utf-8") as f:
            json.dump(token_data, f)

        # Load token
        token, expires_at = auth_manager_production._load_token_from_file()

        assert token is not None, "Token should be loaded from file"
        assert expires_at is not None

        # Verify token is expired (considering 60s buffer)
        is_valid = auth_manager_production._is_token_valid(token, expires_at)
        assert not is_valid, "Token should be considered expired"

    def test_is_token_valid_with_buffer(
        self, auth_manager_production, mock_token_response_data
    ):
        """Test token validation with expiration buffer."""
        # Create token that expires in 30 seconds (within buffer)
        token_data = {
            **mock_token_response_data,
            "expires_in": 30,  # Expires in 30 seconds
        }
        token = TokenResponse(**token_data)
        expires_at = time.time() + 30

        # Should be considered invalid due to 60s buffer
        is_valid = auth_manager_production._is_token_valid(token, expires_at)
        assert not is_valid, "Token should be invalid (within buffer window)"

    @pytest.mark.asyncio
    async def test_get_token_saves_to_file(
        self, auth_manager_production, mock_token_response_data, test_token_storage_path
    ):
        """Test that get_token() saves token to file after fetching."""
        token_file = Path(test_token_storage_path) / "token.json"

        # Mock the HTTP response
        # httpx.Response.json() is a synchronous method, not async
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_token_response_data

        with patch(
            "httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response
        ):
            token_response = await auth_manager_production.get_token()

        # Verify token was saved
        assert token_file.exists(), "Token file should be created"
        assert token_response.access_token == "test-access-token-123"

    @pytest.mark.asyncio
    async def test_get_token_loads_from_file_if_valid(
        self, auth_manager_production, mock_token_response_data, test_token_storage_path
    ):
        """Test that get_token() loads from file if token is still valid."""
        token_file = Path(test_token_storage_path) / "token.json"

        # Pre-save a valid token
        token_data = {
            **mock_token_response_data,
            "saved_at": time.time(),
        }
        with open(token_file, "w", encoding="utf-8") as f:
            json.dump(token_data, f)

        # Should load from file, not make HTTP request
        with patch("httpx.AsyncClient.post") as mock_post:
            token_response = await auth_manager_production.get_token()
            mock_post.assert_not_called()

        assert token_response.access_token == "test-access-token-123"

    def test_clear_stored_token(
        self, auth_manager_production, mock_token_response_data, test_token_storage_path
    ):
        """Test clearing stored token."""
        token_file = Path(test_token_storage_path) / "token.json"

        # Save a token first
        token_response = TokenResponse(**mock_token_response_data)
        auth_manager_production._save_token_to_file(token_response)
        assert token_file.exists()

        # Clear stored token
        auth_manager_production.clear_stored_token()

        # Verify file is deleted and cache is cleared
        assert not token_file.exists(), "Token file should be deleted"
        assert auth_manager_production._cached_token is None
        assert auth_manager_production._token_expires_at is None


def test_environment_auth_url():
    """Test that correct auth URL is used for each environment."""
    from integra_sdk.config import Environment

    # Production URL
    prod_url = Environment.get_auth_url(Environment.PRODUCTION)
    assert prod_url == "https://autenticacao.sapi.serpro.gov.br/authenticate"

    # Trial URL
    trial_url = Environment.get_auth_url(Environment.TRIAL)
    assert trial_url == "https://autenticacao.sapi.serpro.gov.br/authenticate"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
