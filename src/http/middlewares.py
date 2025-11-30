"""HTTP middlewares and hooks for request/response processing."""

from typing import Any, Awaitable, Callable

from typing_extensions import Protocol


class RequestHook(Protocol):
    """Protocol for pre-request hooks."""

    async def __call__(self, method: str, url: str, headers: dict, body: dict) -> None:
        """Called before making a request.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            body: Request body
        """
        ...


class ResponseHook(Protocol):
    """Protocol for post-response hooks."""

    async def __call__(self, response: Any, status_code: int) -> None:
        """Called after receiving a response.

        Args:
            response: Response data
            status_code: HTTP status code
        """
        ...


class MiddlewareManager:
    """Manages request/response hooks."""

    def __init__(self):
        """Initialize middleware manager."""
        self._request_hooks: list[RequestHook] = []
        self._response_hooks: list[ResponseHook] = []

    def add_request_hook(self, hook: RequestHook):
        """Add a pre-request hook.

        Args:
            hook: Hook function to call before requests
        """
        self._request_hooks.append(hook)

    def add_response_hook(self, hook: ResponseHook):
        """Add a post-response hook.

        Args:
            hook: Hook function to call after responses
        """
        self._response_hooks.append(hook)

    async def execute_request_hooks(
        self,
        method: str,
        url: str,
        headers: dict[str, Any],
        body: dict[str, Any],
    ):
        """Execute all pre-request hooks.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            body: Request body
        """
        for hook in self._request_hooks:
            await hook(method, url, headers, body)

    async def execute_response_hooks(self, response: Any, status_code: int):
        """Execute all post-response hooks.

        Args:
            response: Response data
            status_code: HTTP status code
        """
        for hook in self._response_hooks:
            await hook(response, status_code)

