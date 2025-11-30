"""Custom exceptions for the SDK."""


class IntegraSDKError(Exception):
    """Base exception for all SDK errors."""

    pass


class RequestNotFoundError(IntegraSDKError):
    """Raised when a template for the given system/service is not found."""

    def __init__(self, id_sistema: str, id_servico: str):
        self.id_sistema = id_sistema
        self.id_servico = id_servico
        super().__init__(
            f"Template not found for system '{id_sistema}' and service '{id_servico}'"
        )


class ValidationError(IntegraSDKError):
    """Raised when data validation fails."""

    def __init__(self, message: str, errors: dict | None = None):
        self.errors = errors
        super().__init__(message)


class HTTPError(IntegraSDKError):
    """Raised when an HTTP error occurs."""

    def __init__(self, status_code: int, message: str, response_body: str | None = None):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(f"HTTP {status_code}: {message}")


class APIError(IntegraSDKError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int | None = None, response_body: dict | None = None):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class AuthError(IntegraSDKError):
    """Base exception for authentication errors."""

    def __init__(self, message: str, status_code: int | None = None, details: dict | None = None):
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class InvalidCredentialsError(AuthError):
    """Raised when credentials are invalid or authentication fails."""

    pass


class CertificateError(AuthError):
    """Raised when certificate is invalid or not found."""

    pass


class TokenExpiredError(AuthError):
    """Raised when token has expired."""

    pass
