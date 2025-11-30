"""SDK Integra Contador - Comunicação padronizada com a API Integra Contador."""

__version__ = "0.1.0"

# Import templates to register them
from integra_sdk.templates import autenticaproc, caixapostal, dctfweb  # noqa: F401

# Response parsers are no longer used - data is returned in API's original format
# from integra_sdk.responses import autenticaproc, caixapostal  # noqa: F401

from integra_sdk.client import IntegraClient
from integra_sdk.exceptions import (
    APIError,
    AuthError,
    CertificateError,
    HTTPError,
    IntegraSDKError,
    InvalidCredentialsError,
    RequestNotFoundError,
    TokenExpiredError,
    ValidationError,
)

__all__ = [
    "IntegraClient",
    "IntegraSDKError",
    "RequestNotFoundError",
    "ValidationError",
    "APIError",
    "HTTPError",
    "AuthError",
    "InvalidCredentialsError",
    "CertificateError",
    "TokenExpiredError",
]
