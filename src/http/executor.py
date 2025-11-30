"""HTTP request execution."""

import json
import logging
from typing import Any

import httpx

from integra_sdk.config import Environment, IntegraConfig
from integra_sdk.exceptions import APIError, HTTPError
from integra_sdk.http.session import HTTPSession

logger = logging.getLogger(__name__)


class HTTPExecutor:
    """Executes HTTP requests to the Integra Contador API."""

    def __init__(self, config: IntegraConfig, session: HTTPSession | None = None):
        """Initialize HTTP executor.

        Args:
            config: SDK configuration
            session: Optional HTTP session (creates new one if not provided)
        """
        self.config = config
        self.session = session or HTTPSession()

    async def execute(
        self,
        endpoint: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute an HTTP request to the API.

        Args:
            endpoint: API endpoint (e.g., "Consultar", "Emitir")
            body: Request body

        Returns:
            Response data as dictionary

        Raises:
            HTTPError: If HTTP request fails
            APIError: If API returns an error response
        """
        url = f"{self.config.api_base_url}/v1/{endpoint}"

        # Get token from auth_manager if available, otherwise use config token
        jwt_token: str | None = None
        if self.config.auth_manager is not None:
            token_response = await self.config.auth_manager.get_token(self.session.client)
            token = token_response.access_token
            jwt_token = token_response.jwt_token
        else:
            token = self.config.token
            # In production with static token, jwt_token might not be available
            # This is typically only available when using certificate-based auth

        headers = {
            "accept": "text/plain",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Add jwt_token header in production when available (required for production API)
        if jwt_token and self.config.environment == Environment.PRODUCTION:
            headers["jwt_token"] = jwt_token

        # Log request body for debugging (only if logging is enabled)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Request URL: {url}")
            logger.debug(f"Request body: {json.dumps(body, indent=2, ensure_ascii=False)}")

        try:
            response = await self.session.request(
                method="POST",
                url=url,
                headers=headers,
                json=body,
            )

            # Check for HTTP errors
            if response.status_code >= 400:
                try:
                    error_body = response.json()
                except Exception:
                    error_body = response.text

                if response.status_code >= 500:
                    raise HTTPError(
                        status_code=response.status_code,
                        message=f"Server error: {response.status_code}",
                        response_body=error_body,
                    )
                else:
                    raise APIError(
                        message=f"API error: {response.status_code}",
                        status_code=response.status_code,
                        response_body=error_body if isinstance(error_body, dict) else None,
                    )

            # Parse response
            try:
                return response.json()
            except Exception:
                return {"text": response.text}

        except httpx.HTTPStatusError as e:
            raise HTTPError(
                status_code=e.response.status_code,
                message=str(e),
                response_body=e.response.text if e.response else None,
            )
        except httpx.RequestError as e:
            raise HTTPError(
                status_code=0,
                message=f"Request failed: {str(e)}",
                response_body=None,
            )

