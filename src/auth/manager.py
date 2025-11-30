"""Authentication manager for Integra Contador API."""

import base64
import json
import logging
import time
from pathlib import Path
from typing import Any

import httpx
import requests
from requests_pkcs12 import Pkcs12Adapter

from integra_sdk.config import Environment
from integra_sdk.exceptions.errors import (
    AuthError,
    CertificateError,
    HTTPError,
    InvalidCredentialsError,
)
from integra_sdk.types.auth import (
    AuthCredentials,
    AuthErrorResponse,
    CertificateConfig,
    SavedAuthConfig,
    TokenResponse,
)

logger = logging.getLogger(__name__)


class AuthManager:
    """Manages authentication and token caching for Integra Contador API."""

    ROLE_TYPE = "TERCEIROS"

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        certificate_path: str,
        certificate_password: str,
        environment: Environment | str | None = None,
        token_storage_path: Path | str | None = None,
    ):
        """Initialize authentication manager.

        Args:
            consumer_key: Consumer key (API key) for Basic Auth header
            consumer_secret: Consumer secret (API secret) for Basic Auth header
            certificate_path: Path to certificate file (.p12) - REQUIRED
            certificate_password: Certificate password - REQUIRED
            environment: Environment (Trial or Production) to determine auth URL
            token_storage_path: Optional custom path for token storage. If not provided,
                              uses .auth/ directory relative to SDK package

        Raises:
            ValueError: If credentials are invalid or certificate file doesn't exist

        Note:
            The certificate is REQUIRED for authentication. The Basic Auth (consumer_key/secret)
            is used to identify the application, but the certificate digital is mandatory for
            authenticating with the API.
        """
        # Validate and store credentials
        self.credentials = AuthCredentials(
            consumer_key=consumer_key, consumer_secret=consumer_secret
        )

        # Certificate is REQUIRED
        if not certificate_path:
            raise ValueError(
                "Certificate path is required. Authentication requires a digital certificate (.p12 file)."
            )
        if not certificate_password:
            raise ValueError("Certificate password is required.")

        self.certificate = CertificateConfig(
            path=certificate_path, password=certificate_password
        )

        # Validate that certificate file exists
        cert_file = Path(self.certificate.path)
        if not cert_file.exists():
            raise ValueError(f"Certificate file not found: {certificate_path}")
        if not cert_file.is_file():
            raise ValueError(f"Certificate path is not a file: {certificate_path}")

        # Set environment and auth URL
        if environment is None:
            environment = Environment.PRODUCTION  # Default to production
        elif isinstance(environment, str):
            environment = Environment(environment)
        self.environment = environment
        self.auth_url = Environment.get_auth_url(self.environment)

        # Set token storage path
        if token_storage_path is None:
            # Default to .auth/ in SDK package directory
            # Try to find SDK root (where src/ is)
            sdk_root = Path(__file__).parent.parent.parent
            if (sdk_root / "src").exists():
                # We're in the SDK source directory
                self.token_storage_dir = sdk_root / ".auth"
            else:
                # Fallback: use user home directory
                home = Path.home()
                self.token_storage_dir = home / ".integra_sdk" / ".auth"
        else:
            self.token_storage_dir = Path(token_storage_path)

        # Ensure token storage directory exists
        self.token_storage_dir.mkdir(parents=True, exist_ok=True)
        self.token_file_path = self.token_storage_dir / "token.json"
        self.config_file_path = self.token_storage_dir / "config.json"

        # Token cache
        self._cached_token: TokenResponse | None = None
        self._token_expires_at: float | None = None

        # Save configuration automatically for Production environment
        if self.environment == Environment.PRODUCTION:
            self.save_config()

    def _get_basic_auth_header(self) -> str:
        """Generate Basic authentication header.

        Returns:
            Authorization header string in format "Basic {base64_encoded}"
        """
        credentials = (
            f"{self.credentials.consumer_key}:{self.credentials.consumer_secret}"
        )
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return f"Basic {encoded}"

    def _build_auth_headers(self) -> dict[str, str]:
        """Build headers for authentication request.

        Returns:
            Dictionary with authentication headers
        """
        return {
            "Authorization": self._get_basic_auth_header(),
            "Role-Type": self.ROLE_TYPE,
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _build_auth_body(self) -> dict[str, str]:
        """Build body for authentication request.

        Returns:
            Dictionary with form data
        """
        return {"grant_type": "client_credentials"}

    def _is_token_valid(
        self, token: TokenResponse | None = None, expires_at: float | None = None
    ) -> bool:
        """Check if token is still valid.

        Args:
            token: TokenResponse to check (uses cached token if None)
            expires_at: Expiration timestamp (uses cached expiration if None)

        Returns:
            True if token exists and is not expired, False otherwise
        """
        token_to_check = token if token is not None else self._cached_token
        expires_at_to_check = (
            expires_at if expires_at is not None else self._token_expires_at
        )

        if token_to_check is None or expires_at_to_check is None:
            return False

        # Add a 60 second buffer before expiration
        buffer_seconds = 60
        return time.time() < (expires_at_to_check - buffer_seconds)

    def _save_token_to_file(self, token_response: TokenResponse) -> None:
        """Save token response to JSON file.

        Args:
            token_response: TokenResponse to save
        """
        try:
            token_data = {
                "expires_in": token_response.expires_in,
                "scope": token_response.scope,
                "token_type": token_response.token_type,
                "access_token": token_response.access_token,
                "jwt_token": token_response.jwt_token,
                "jwt_pucomex": token_response.jwt_pucomex,
                "saved_at": time.time(),
            }

            with open(self.token_file_path, "w", encoding="utf-8") as f:
                json.dump(token_data, f, indent=2)

            logger.debug(f"Token saved to {self.token_file_path}")
        except Exception as e:
            logger.warning(f"Failed to save token to file: {e}", exc_info=True)

    def _load_token_from_file(self) -> tuple[TokenResponse | None, float | None]:
        """Load token response from JSON file.

        Returns:
            Tuple of (TokenResponse, expires_at timestamp) or (None, None) if not found/invalid
        """
        if not self.token_file_path.exists():
            logger.debug("No token file found")
            return None, None

        try:
            with open(self.token_file_path, "r", encoding="utf-8") as f:
                token_data = json.load(f)

            # Validate required fields
            required_fields = ["expires_in", "access_token", "jwt_token", "token_type"]
            if not all(field in token_data for field in required_fields):
                logger.warning("Token file missing required fields")
                return None, None

            # Recreate TokenResponse
            token_response = TokenResponse(
                expires_in=token_data["expires_in"],
                scope=token_data.get("scope", "default"),
                token_type=token_data["token_type"],
                access_token=token_data["access_token"],
                jwt_token=token_data["jwt_token"],
                jwt_pucomex=token_data.get("jwt_pucomex"),
            )

            # Calculate expiration time
            saved_at = token_data.get("saved_at", time.time())
            expires_at = saved_at + token_response.expires_in

            logger.debug(f"Token loaded from {self.token_file_path}")
            return token_response, expires_at

        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in token file: {e}")
            return None, None
        except Exception as e:
            logger.warning(f"Failed to load token from file: {e}", exc_info=True)
            return None, None

    async def get_token(
        self, session: httpx.AsyncClient | None = None
    ) -> TokenResponse:
        """Get authentication token (from cache, file, or API).

        Note: The session parameter is kept for API compatibility but is not used
        for authentication requests, as we use requests library for .p12 certificate support.
        """
        """Get authentication token (from cache, file, or API).

        Args:
            session: Optional httpx.AsyncClient instance. If not provided, creates a new one.

        Returns:
            TokenResponse with access_token and jwt_token

        Raises:
            CertificateError: When certificate is invalid or not found (400)
            InvalidCredentialsError: When credentials are invalid (401)
            AuthError: For other authentication errors
            HTTPError: For HTTP connection errors

        Examples:
            >>> manager = AuthManager("key", "secret")
            >>> token = await manager.get_token()
            >>> print(token.access_token)
        """
        # Check in-memory cache first
        if self._is_token_valid() and self._cached_token:
            logger.debug("Using cached token from memory")
            return self._cached_token

        # Try to load from file
        file_token, file_expires_at = self._load_token_from_file()
        if file_token and self._is_token_valid(file_token, file_expires_at):
            logger.debug("Using token from file")
            # Update cache
            self._cached_token = file_token
            self._token_expires_at = file_expires_at
            return file_token

        # Token not valid in cache or file, fetch new one
        logger.debug("Fetching new token from API")

        # Build request components
        headers = self._build_auth_headers()
        data = self._build_auth_body()

        # Certificate is always required
        # httpx doesn't support .p12 directly, so we use requests for auth
        # This is the only synchronous operation, everything else uses httpx
        try:
            # Convert data dict to form-urlencoded string
            form_data = "&".join([f"{k}={v}" for k, v in data.items()])

            # Use requests with Pkcs12Adapter for .p12 certificate support
            session = requests.Session()
            session.mount(
                self.auth_url,
                Pkcs12Adapter(
                    pkcs12_filename=self.certificate.path,
                    pkcs12_password=self.certificate.password,
                ),
            )

            response = session.post(
                self.auth_url,
                headers=headers,
                data=form_data,
                timeout=30.0,
            )

            # Handle response
            if response.status_code == 200:
                # Parse successful response
                response_data = response.json()
                token_response = TokenResponse(**response_data)

                # Cache token in memory
                self._cached_token = token_response
                self._token_expires_at = time.time() + token_response.expires_in

                # Save token to file
                self._save_token_to_file(token_response)

                # Ensure config is saved (in case it wasn't saved during init)
                if self.environment == Environment.PRODUCTION:
                    self.save_config()

                return token_response

            elif response.status_code == 400:
                # Certificate error
                try:
                    error_data = response.json()
                    error_response = AuthErrorResponse(**error_data)
                    message = error_response.message
                except Exception:
                    message = (
                        "Não foi possível identificar um certificado digital válido."
                    )

                raise CertificateError(
                    message=message,
                    status_code=400,
                    details={"response": response.text},
                )

            elif response.status_code in (401, 403):
                # Invalid credentials
                try:
                    error_data = response.json()
                    error_response = AuthErrorResponse(**error_data)
                    message = error_response.message
                except Exception:
                    message = "Credenciais inválidas."

                raise InvalidCredentialsError(
                    message=message,
                    status_code=response.status_code,
                    details={"response": response.text},
                )

            else:
                # Other errors
                try:
                    error_data = response.json()
                    error_response = AuthErrorResponse(**error_data)
                    message = error_response.message
                except Exception:
                    message = (
                        f"Authentication failed with status {response.status_code}"
                    )

                raise AuthError(
                    message=message,
                    status_code=response.status_code,
                    details={"response": response.text},
                )

        except (InvalidCredentialsError, CertificateError, AuthError):
            # Re-raise auth-specific errors
            raise
        except requests.exceptions.RequestException as e:
            # Wrap HTTP errors from requests
            status_code = (
                getattr(e.response, "status_code", 0) if hasattr(e, "response") else 0
            )
            raise HTTPError(
                status_code=status_code,
                message=f"HTTP error during authentication: {str(e)}",
                response_body=None,
            ) from e
        except Exception as e:
            # Wrap any other errors
            raise HTTPError(
                status_code=0,
                message=f"Unexpected error during authentication: {str(e)}",
                response_body=None,
            ) from e

    def clear_cache(self) -> None:
        """Clear cached token (force next request to fetch new token)."""
        self._cached_token = None
        self._token_expires_at = None

    def clear_stored_token(self) -> None:
        """Clear stored token file and cache (force next request to fetch new token)."""
        self.clear_cache()
        try:
            if self.token_file_path.exists():
                self.token_file_path.unlink()
                logger.debug(f"Token file deleted: {self.token_file_path}")
        except Exception as e:
            logger.warning(f"Failed to delete token file: {e}", exc_info=True)

    def save_config(self) -> None:
        """Save authentication configuration to file.
        
        This saves the credentials (consumer_key, consumer_secret, certificate_path,
        certificate_password) and environment to allow automatic loading in future sessions.
        """
        try:
            config_data = SavedAuthConfig(
                consumer_key=self.credentials.consumer_key,
                consumer_secret=self.credentials.consumer_secret,
                certificate_path=self.certificate.path,
                certificate_password=self.certificate.password,
                environment=self.environment.value,
                saved_at=time.time(),
            )

            with open(self.config_file_path, "w", encoding="utf-8") as f:
                json.dump(config_data.model_dump(), f, indent=2)

            logger.debug(f"Auth config saved to {self.config_file_path}")
        except Exception as e:
            logger.warning(f"Failed to save auth config to file: {e}", exc_info=True)

    @classmethod
    def load_config(
        cls, token_storage_path: Path | str | None = None
    ) -> SavedAuthConfig | None:
        """Load saved authentication configuration from file.

        Args:
            token_storage_path: Optional custom path for token storage. If not provided,
                              uses .auth/ directory relative to SDK package

        Returns:
            SavedAuthConfig if found and valid, None otherwise
        """
        # Determine config file path
        if token_storage_path is None:
            # Default to .auth/ in SDK package directory
            sdk_root = Path(__file__).parent.parent.parent
            if (sdk_root / "src").exists():
                config_dir = sdk_root / ".auth"
            else:
                home = Path.home()
                config_dir = home / ".integra_sdk" / ".auth"
        else:
            config_dir = Path(token_storage_path)

        config_file_path = config_dir / "config.json"

        if not config_file_path.exists():
            logger.debug("No auth config file found")
            return None

        try:
            with open(config_file_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            # Validate required fields
            required_fields = [
                "consumer_key",
                "consumer_secret",
                "certificate_path",
                "certificate_password",
                "environment",
            ]
            if not all(field in config_data for field in required_fields):
                logger.warning("Config file missing required fields")
                return None

            # Recreate SavedAuthConfig
            saved_config = SavedAuthConfig(**config_data)

            logger.debug(f"Auth config loaded from {config_file_path}")
            return saved_config

        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in config file: {e}")
            return None
        except Exception as e:
            logger.warning(f"Failed to load auth config from file: {e}", exc_info=True)
            return None

    @classmethod
    def from_saved_config(
        cls,
        token_storage_path: Path | str | None = None,
        environment: Environment | str | None = None,
    ) -> "AuthManager | None":
        """Create AuthManager from saved configuration.

        Args:
            token_storage_path: Optional custom path for token storage
            environment: Optional environment override (must match saved config if provided)

        Returns:
            AuthManager instance if config found and valid, None otherwise
        """
        saved_config = cls.load_config(token_storage_path)
        if saved_config is None:
            return None

        # If environment specified, verify it matches
        if environment is not None:
            if isinstance(environment, str):
                environment = Environment(environment)
            if environment.value != saved_config.environment:
                logger.warning(
                    f"Saved config environment ({saved_config.environment}) "
                    f"does not match requested environment ({environment.value})"
                )
                return None

        # Verify certificate file still exists
        cert_file = Path(saved_config.certificate_path)
        if not cert_file.exists():
            logger.warning(
                f"Certificate file from saved config not found: {saved_config.certificate_path}"
            )
            return None

        # Create AuthManager with saved config
        auth_manager = cls(
            consumer_key=saved_config.consumer_key,
            consumer_secret=saved_config.consumer_secret,
            certificate_path=saved_config.certificate_path,
            certificate_password=saved_config.certificate_password,
            environment=saved_config.environment,
            token_storage_path=token_storage_path,
        )

        logger.info("AuthManager created from saved configuration")
        return auth_manager
