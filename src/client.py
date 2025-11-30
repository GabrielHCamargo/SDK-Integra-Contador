"""Main client for Integra Contador API."""

import logging
from typing import Any

from integra_sdk.auth.manager import AuthManager

logger = logging.getLogger(__name__)
from integra_sdk.builder.request_builder import RequestBuilder
from integra_sdk.builder.response_builder import ResponseBuilder
from integra_sdk.config import IntegraConfig, Environment
from integra_sdk.http.executor import HTTPExecutor
from integra_sdk.http.session import HTTPSession

# Import templates to register them
from integra_sdk.templates import autenticaproc, caixapostal, dctfweb  # noqa: F401

# Response parsers are no longer used - data is returned in API's original format
# from integra_sdk.responses import autenticaproc, caixapostal  # noqa: F401


class IntegraClient:
    """Client for Integra Contador API."""

    def __init__(
        self,
        environment: str | Environment,
        config: dict[str, Any],
        token: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        # Authentication credentials with certificate (alternative to token)
        consumer_key: str | None = None,
        consumer_secret: str | None = None,
        certificate_path: str | None = None,
        certificate_password: str | None = None,
    ):
        """Initialize Integra Client.

        Args:
            environment: Environment name ("Trial" or "Production")
            config: Configuration dictionary with contratante, contribuinte, autorPedidoDados
            token: Bearer token for authentication (optional for Trial, required for Production)
            base_url: Optional custom base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            consumer_key: Optional consumer key for authentication (alternative to token)
            consumer_secret: Optional consumer secret for authentication (alternative to token)
            certificate_path: Optional path to certificate file (.p12) for authentication
            certificate_password: Optional certificate password

        Note:
            - In Trial environment, if token is not provided, a default trial token will be used
            - In Production environment, token is required (unless using certificate-based authentication)
            - If consumer_key/consumer_secret are provided, certificate_path and certificate_password are REQUIRED
            - Authentication with certificate requires ALL four parameters: consumer_key, consumer_secret, certificate_path, certificate_password
        """
        # Convert environment string to Environment enum if needed
        env = environment
        if isinstance(env, str):
            env = Environment(env)

        # Create AuthManager if credentials provided (certificate is REQUIRED)
        # Note: Trial environment does not use authentication
        auth_manager = None

        # For Production environment, try to load saved config first
        if env == Environment.PRODUCTION:
            # Try to load from saved config if no credentials provided
            if not (
                consumer_key
                or consumer_secret
                or certificate_path
                or certificate_password
            ):
                saved_auth_manager = AuthManager.from_saved_config(environment=env)
                if saved_auth_manager is not None:
                    auth_manager = saved_auth_manager
                    logger.info(
                        "Using saved authentication configuration for Production"
                    )
                else:
                    # No saved config and no credentials provided - raise error
                    raise ValueError(
                        "Production environment requires authentication credentials. "
                        "Please provide consumer_key, consumer_secret, certificate_path, and certificate_password, "
                        "or ensure you have previously saved credentials using these parameters."
                    )

        # If credentials are explicitly provided, use them (overrides saved config)
        if consumer_key or consumer_secret or certificate_path or certificate_password:
            # In Trial environment, authentication is not used
            if env == Environment.TRIAL:
                raise ValueError(
                    "Authentication is not required for Trial environment. "
                    "Please remove consumer_key, consumer_secret, certificate_path, and certificate_password parameters."
                )

            # If any auth parameter is provided, all are required
            if not all(
                [consumer_key, consumer_secret, certificate_path, certificate_password]
            ):
                raise ValueError(
                    "All authentication parameters are required: consumer_key, consumer_secret, "
                    "certificate_path, and certificate_password must all be provided together."
                )

            auth_manager = AuthManager(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                certificate_path=certificate_path,
                certificate_password=certificate_password,
                environment=env,
            )

        self.config = IntegraConfig.from_dict(
            environment, config, token, base_url, auth_manager=auth_manager
        )
        self.session = HTTPSession(timeout=timeout, max_retries=max_retries)
        self.executor = HTTPExecutor(self.config, self.session)

    async def _execute(
        self,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a request using template and data.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            API response data
        """
        # Build request
        template, request_body = RequestBuilder.build(
            self.config,
            id_sistema,
            id_servico,
            dados,
        )

        # Execute request
        endpoint = template.get_endpoint()
        raw_response = await self.executor.execute(endpoint, request_body)

        # Parse and structure response
        structured_response = ResponseBuilder.build(
            id_sistema, id_servico, raw_response
        )

        return structured_response

    async def consultar(
        self,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a Consultar request.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            API response data
        """
        return await self._execute(id_sistema, id_servico, dados)

    async def emitir(
        self,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute an Emitir request.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            API response data
        """
        return await self._execute(id_sistema, id_servico, dados)

    async def transmitir(
        self,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a Transmitir request.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            API response data
        """
        return await self._execute(id_sistema, id_servico, dados)

    async def declarar(
        self,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a Declarar request.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            API response data
        """
        return await self._execute(id_sistema, id_servico, dados)

    async def apoiar(
        self,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute an Apoiar request.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            API response data
        """
        return await self._execute(id_sistema, id_servico, dados)

    async def monitorar(
        self,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a Monitorar request.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            API response data
        """
        return await self._execute(id_sistema, id_servico, dados)

    async def authenticate(self) -> dict[str, Any]:
        """Manually authenticate and get token (optional helper method).

        Returns:
            Token response with access_token and jwt_token

        Raises:
            AuthError: If authentication fails

        Note:
            This method is only available when using consumer_key/consumer_secret.
            It's useful for debugging or advanced use cases.
        """
        if self.config.auth_manager is None:
            raise ValueError(
                "AuthManager not configured. Please provide consumer_key and consumer_secret."
            )

        token_response = await self.config.auth_manager.get_token(self.session.client)
        return {
            "access_token": token_response.access_token,
            "jwt_token": token_response.jwt_token,
            "expires_in": token_response.expires_in,
            "token_type": token_response.token_type,
            "scope": token_response.scope,
        }

    async def close(self):
        """Close the HTTP session."""
        await self.session.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
