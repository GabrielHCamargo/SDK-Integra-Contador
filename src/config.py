"""Configuration and context for the SDK."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from integra_sdk.types.common import AutorPedidoDados, Contratante, Contribuinte

# Token fixo para ambiente Trial
TRIAL_TOKEN = "06aef429-a981-3ec5-a1f8-71d38d86481e"

# URLs de autenticação por ambiente
# Nota: O ambiente Trial não requer autenticação (não usa AuthManager)
# A URL de Trial é mantida apenas para referência futura, caso necessário
AUTH_URL_TRIAL = "https://autenticacao.sapi.serpro.gov.br/authenticate"
AUTH_URL_PRODUCTION = "https://autenticacao.sapi.serpro.gov.br/authenticate"


class Environment(str, Enum):
    """API environment."""

    TRIAL = "Trial"
    PRODUCTION = "Production"

    @classmethod
    def get_auth_url(cls, environment: "Environment | str") -> str:
        """Get authentication URL for the given environment.

        Args:
            environment: Environment instance or string name

        Returns:
            Authentication URL string
        """
        if isinstance(environment, str):
            environment = cls(environment)

        if environment == cls.TRIAL:
            return AUTH_URL_TRIAL
        elif environment == cls.PRODUCTION:
            return AUTH_URL_PRODUCTION
        else:
            raise ValueError(f"Unknown environment: {environment}")


class IntegraConfig(BaseModel):
    """Configuration for Integra Contador API."""

    environment: Environment = Field(
        default=Environment.TRIAL, description="API environment"
    )
    contratante: Contratante = Field(..., description="Contractor information")
    contribuinte: Contribuinte = Field(..., description="Taxpayer information")
    autorPedidoDados: AutorPedidoDados = Field(
        ..., description="Request author information"
    )
    token: str = Field(..., description="Bearer token for authentication")
    base_url: str | None = Field(default=None, description="Custom base URL (optional)")
    auth_manager: Any = Field(
        default=None,
        description="Optional AuthManager instance for automatic token management",
    )

    @property
    def api_base_url(self) -> str:
        """Get the base URL for the API based on environment."""
        if self.base_url:
            return self.base_url

        if self.environment == Environment.TRIAL:
            return "https://gateway.apiserpro.serpro.gov.br/integra-contador-trial"
        elif self.environment == Environment.PRODUCTION:
            return "https://gateway.apiserpro.serpro.gov.br/integra-contador"
        else:
            raise ValueError(f"Unknown environment: {self.environment}")

    @classmethod
    def from_dict(
        cls,
        environment: str | Environment,
        config: dict,
        token: str | None = None,
        base_url: str | None = None,
        auth_manager: Any = None,
    ) -> "IntegraConfig":
        """Create config from dictionary.

        Args:
            environment: Environment name ("Trial" or "Production")
            config: Configuration dictionary with contratante, contribuinte, autorPedidoDados
            token: Bearer token for authentication (optional for Trial, required for Production)
            base_url: Optional custom base URL
            auth_manager: Optional AuthManager instance for automatic token management

        Returns:
            IntegraConfig instance

        Raises:
            ValueError: If token is required but not provided
        """
        if isinstance(environment, str):
            environment = Environment(environment)

        # Se auth_manager fornecido, token pode ser None (será obtido dinamicamente)
        if auth_manager is not None:
            # Token será obtido automaticamente do auth_manager
            final_token = token if token is not None else ""
        else:
            # Em Trial, usar token fixo se não fornecido
            if environment == Environment.TRIAL:
                final_token = token if token is not None else TRIAL_TOKEN
            else:
                # Em Produção, token é obrigatório se não há auth_manager
                if token is None or not token.strip():
                    raise ValueError(
                        "Token is required for Production environment. "
                        "Please provide a valid Bearer token or an AuthManager instance."
                    )
                final_token = token

        return cls(
            environment=environment,
            contratante=Contratante(**config["contratante"]),
            contribuinte=Contribuinte(**config["contribuinte"]),
            autorPedidoDados=AutorPedidoDados(**config["autorPedidoDados"]),
            token=final_token,
            base_url=base_url,
            auth_manager=auth_manager,
        )
