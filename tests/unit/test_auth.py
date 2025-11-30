"""Unit tests for authentication module."""

import asyncio
import base64
import time
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from integra_sdk.auth.manager import AuthManager
from integra_sdk.exceptions.errors import (
    AuthError,
    CertificateError,
    HTTPError,
    InvalidCredentialsError,
)
from integra_sdk.types.auth import AuthErrorResponse, TokenResponse


@pytest.fixture
def test_certificate_path(tmp_path):
    """Fixture creating a dummy certificate file."""
    cert_file = tmp_path / "test_cert.p12"
    cert_file.write_bytes(b"dummy certificate data")
    return str(cert_file)


@pytest.fixture
def test_credentials():
    """Fixture with test credentials."""
    return {
        "consumer_key": "test_key",
        "consumer_secret": "test_secret",
        "certificate_password": "test_password",
    }


@pytest.fixture
def auth_manager(test_credentials, test_certificate_path):
    """Fixture creating an AuthManager instance."""
    return AuthManager(
        consumer_key=test_credentials["consumer_key"],
        consumer_secret=test_credentials["consumer_secret"],
        certificate_path=test_certificate_path,
        certificate_password=test_credentials["certificate_password"],
    )


@pytest.fixture
def mock_token_response():
    """Fixture with mock token response data."""
    return {
        "expires_in": 2008,
        "scope": "default",
        "token_type": "Bearer",
        "access_token": "test-access-token",
        "jwt_token": "test-jwt-token",
        "jwt_pucomex": None,
    }


class TestAuthManagerBasicAuth:
    """Test Basic authentication header generation."""

    def test_get_basic_auth_header(self, auth_manager):
        """Test that basic auth header is generated correctly."""
        header = auth_manager._get_basic_auth_header()

        # Should start with "Basic "
        assert header.startswith("Basic ")

        # Decode and verify
        encoded = header.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        assert decoded == "test_key:test_secret"

    def test_get_basic_auth_header_with_cert(
        self, test_credentials, test_certificate_path
    ):
        """Test basic auth header generation with certificate."""
        manager = AuthManager(
            consumer_key=test_credentials["consumer_key"],
            consumer_secret=test_credentials["consumer_secret"],
            certificate_path=test_certificate_path,
            certificate_password=test_credentials["certificate_password"],
        )
        header = manager._get_basic_auth_header()
        assert header.startswith("Basic ")

    def test_build_auth_headers(self, auth_manager):
        """Test that auth headers are built correctly."""
        headers = auth_manager._build_auth_headers()

        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")
        assert headers["Role-Type"] == "TERCEIROS"
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"

    def test_build_auth_body(self, auth_manager):
        """Test that auth body is built correctly."""
        body = auth_manager._build_auth_body()

        assert body == {"grant_type": "client_credentials"}


class TestAuthManagerInitialization:
    """Test AuthManager initialization."""

    def test_init_with_credentials_and_certificate(
        self, test_credentials, test_certificate_path
    ):
        """Test initialization with credentials and certificate."""
        manager = AuthManager(
            consumer_key=test_credentials["consumer_key"],
            consumer_secret=test_credentials["consumer_secret"],
            certificate_path=test_certificate_path,
            certificate_password=test_credentials["certificate_password"],
        )
        assert manager.credentials.consumer_key == "test_key"
        assert manager.credentials.consumer_secret == "test_secret"
        assert manager.certificate is not None
        assert manager.certificate.path == str(test_certificate_path)

    def test_init_without_certificate_raises_error(self, test_credentials):
        """Test that missing certificate raises error."""
        with pytest.raises(ValueError, match="Certificate path is required"):
            AuthManager(
                consumer_key=test_credentials["consumer_key"],
                consumer_secret=test_credentials["consumer_secret"],
                certificate_path="",
                certificate_password=test_credentials["certificate_password"],
            )

    def test_init_without_certificate_password_raises_error(
        self, test_credentials, test_certificate_path
    ):
        """Test that missing certificate password raises error."""
        with pytest.raises(ValueError, match="password is required"):
            AuthManager(
                consumer_key=test_credentials["consumer_key"],
                consumer_secret=test_credentials["consumer_secret"],
                certificate_path=test_certificate_path,
                certificate_password="",
            )

    def test_init_empty_credentials_raises_error(self, test_certificate_path):
        """Test that empty credentials raise validation error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            AuthManager(
                consumer_key="",
                consumer_secret="test_secret",
                certificate_path=test_certificate_path,
                certificate_password="pass",
            )

        with pytest.raises(ValueError, match="cannot be empty"):
            AuthManager(
                consumer_key="test_key",
                consumer_secret="",
                certificate_path=test_certificate_path,
                certificate_password="pass",
            )

    def test_init_certificate_not_found_raises_error(self, test_credentials):
        """Test that missing certificate file raises error."""
        with pytest.raises(ValueError, match="not found"):
            AuthManager(
                consumer_key=test_credentials["consumer_key"],
                consumer_secret=test_credentials["consumer_secret"],
                certificate_path="/nonexistent/cert.p12",
                certificate_password=test_credentials["certificate_password"],
            )


class TestAuthManagerGetToken:
    """Test token retrieval."""

    @pytest.mark.asyncio
    async def test_get_token_success(self, auth_manager, mock_token_response):
        """Test successful token retrieval."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_token_response

        # Mock httpx client
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client

            # Get token
            token_response = await auth_manager.get_token()

            # Verify response
            assert isinstance(token_response, TokenResponse)
            assert token_response.access_token == "test-access-token"
            assert token_response.jwt_token == "test-jwt-token"
            assert token_response.expires_in == 2008

            # Verify cache was set
            assert auth_manager._cached_token is not None
            assert auth_manager._token_expires_at is not None

    @pytest.mark.asyncio
    async def test_get_token_with_session(self, auth_manager, mock_token_response):
        """Test token retrieval with provided session."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_token_response

        mock_session = AsyncMock()
        mock_session.post = AsyncMock(return_value=mock_response)

        token_response = await auth_manager.get_token(session=mock_session)

        assert token_response.access_token == "test-access-token"
        # Session should not be closed since we didn't create it
        assert not hasattr(mock_session, "aclose") or not mock_session.aclose.called

    @pytest.mark.asyncio
    async def test_get_token_error_400(self, auth_manager):
        """Test token retrieval with 400 error (certificate error)."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "timestamp": "2025-11-24 20:55:52",
            "status": 400,
            "error": "Bad Request",
            "message": "Não foi possível identificar um certificado digital válido.",
            "details": [],
            "trackerId": "jvBQVbAq",
            "path": "/authenticate",
        }
        mock_response.text = '{"error": "Bad Request"}'

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client

            with pytest.raises(CertificateError) as exc_info:
                await auth_manager.get_token()

            assert exc_info.value.status_code == 400
            assert "certificado" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_get_token_error_401(self, auth_manager):
        """Test token retrieval with 401 error (invalid credentials)."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "timestamp": "2025-11-24 20:55:52",
            "status": 401,
            "error": "Unauthorized",
            "message": "Credenciais inválidas.",
            "details": [],
            "path": "/authenticate",
        }
        mock_response.text = '{"error": "Unauthorized"}'

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client

            with pytest.raises(InvalidCredentialsError) as exc_info:
                await auth_manager.get_token()

            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_get_token_error_403(self, auth_manager):
        """Test token retrieval with 403 error."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "status": 403,
            "message": "Forbidden",
        }
        mock_response.text = '{"error": "Forbidden"}'

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client

            with pytest.raises(InvalidCredentialsError) as exc_info:
                await auth_manager.get_token()

            assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_get_token_http_error(self, auth_manager):
        """Test token retrieval with HTTP connection error."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(
                side_effect=httpx.NetworkError("Connection error")
            )
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client

            with pytest.raises(HTTPError) as exc_info:
                await auth_manager.get_token()

            assert "Connection error" in str(exc_info.value)


class TestAuthManagerTokenCache:
    """Test token caching functionality."""

    @pytest.mark.asyncio
    async def test_token_caching(self, auth_manager, mock_token_response):
        """Test that token is cached and reused."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_token_response

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client

            # First call - should make HTTP request
            token1 = await auth_manager.get_token()
            assert mock_client.post.call_count == 1

            # Second call - should use cache
            token2 = await auth_manager.get_token()
            assert mock_client.post.call_count == 1  # Still only 1 call
            assert token1.access_token == token2.access_token

    @pytest.mark.asyncio
    async def test_token_cache_expiry(self, auth_manager):
        """Test that expired tokens trigger new request."""
        # First response with short expiry
        mock_response1 = MagicMock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {
            "expires_in": 2,  # Very short expiry (2 seconds)
            "scope": "default",
            "token_type": "Bearer",
            "access_token": "token1",
            "jwt_token": "jwt1",
            "jwt_pucomex": None,
        }

        # Second response
        mock_response2 = MagicMock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {
            "expires_in": 2008,
            "scope": "default",
            "token_type": "Bearer",
            "access_token": "token2",
            "jwt_token": "jwt2",
            "jwt_pucomex": None,
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(side_effect=[mock_response1, mock_response2])
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client

            # First call
            token1 = await auth_manager.get_token()
            assert token1.access_token == "token1"
            assert mock_client.post.call_count == 1

            # Wait for token to expire (with buffer)
            await asyncio.sleep(3)

            # Second call - should fetch new token
            token2 = await auth_manager.get_token()
            assert token2.access_token == "token2"
            assert mock_client.post.call_count == 2

    def test_clear_cache(self, auth_manager):
        """Test cache clearing."""
        # Set some cached values
        auth_manager._cached_token = TokenResponse(
            expires_in=2008,
            scope="default",
            token_type="Bearer",
            access_token="test",
            jwt_token="test",
            jwt_pucomex=None,
        )
        auth_manager._token_expires_at = time.time() + 2008

        # Clear cache
        auth_manager.clear_cache()

        assert auth_manager._cached_token is None
        assert auth_manager._token_expires_at is None

    def test_is_token_valid(self, auth_manager):
        """Test token validity check."""
        # No token cached
        assert not auth_manager._is_token_valid()

        # Valid token cached
        auth_manager._cached_token = TokenResponse(
            expires_in=2008,
            scope="default",
            token_type="Bearer",
            access_token="test",
            jwt_token="test",
            jwt_pucomex=None,
        )
        auth_manager._token_expires_at = time.time() + 2008
        assert auth_manager._is_token_valid()

        # Expired token
        auth_manager._token_expires_at = time.time() - 10
        assert not auth_manager._is_token_valid()
