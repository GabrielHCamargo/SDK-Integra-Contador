"""HTTP session management with retries and timeout."""

import asyncio
from typing import Any

import httpx


class HTTPSession:
    """HTTP session with retries and timeout configuration."""

    def __init__(
        self,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_backoff: float = 1.0,
    ):
        """Initialize HTTP session.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_backoff: Backoff multiplier for retries
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            json: JSON body

        Returns:
            HTTP response

        Raises:
            httpx.HTTPError: If request fails after retries
        """
        last_exception = None
        backoff = self.retry_backoff

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json,
                )
                return response
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                else:
                    raise
            except httpx.HTTPStatusError as e:
                # Don't retry on HTTP errors (4xx, 5xx)
                raise

        if last_exception:
            raise last_exception

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

