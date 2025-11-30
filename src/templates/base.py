"""Base template class for request templates."""

from abc import ABC, abstractmethod
from typing import Any

from integra_sdk.config import IntegraConfig
from integra_sdk.exceptions import ValidationError


class BaseTemplate(ABC):
    """Base class for all request templates."""

    def __init__(self, id_sistema: str, id_servico: str, versao_sistema: str = "1.0"):
        """Initialize template.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            versao_sistema: System version
        """
        self.id_sistema = id_sistema
        self.id_servico = id_servico
        self.versao_sistema = versao_sistema

    @abstractmethod
    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary

        Returns:
            Validated and normalized data

        Raises:
            ValidationError: If validation fails
        """
        pass

    @abstractmethod
    def get_endpoint(self) -> str:
        """Get the API endpoint for this template.

        Returns:
            Endpoint name (e.g., "Consultar", "Emitir")
        """
        pass

    def build_request(
        self,
        config: IntegraConfig,
        dados: dict[str, Any],
    ) -> dict[str, Any]:
        """Build the complete request body.

        Args:
            config: SDK configuration
            dados: Service-specific data

        Returns:
            Complete request body dictionary
        """
        # Validate data
        validated_dados = self.validate(dados)

        # Build request body
        return {
            "contratante": config.contratante.model_dump(),
            "autorPedidoDados": config.autorPedidoDados.model_dump(),
            "contribuinte": config.contribuinte.model_dump(),
            "pedidoDados": {
                "idSistema": self.id_sistema,
                "idServico": self.id_servico,
                "versaoSistema": self.versao_sistema,
                "dados": self._serialize_dados(validated_dados),
            },
        }

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados dictionary to JSON string.

        Args:
            dados: Data dictionary

        Returns:
            JSON string (compact format without spaces)
        """
        import json

        # Use separators to ensure compact JSON format without spaces
        # This matches the API's expected format: {"key":"value"} instead of {"key" : "value"}
        return json.dumps(dados, ensure_ascii=False, separators=(',', ':'))

    def _validate_required_fields(
        self,
        dados: dict[str, Any],
        required_fields: list[str],
    ) -> None:
        """Validate that required fields are present.

        Args:
            dados: Data dictionary
            required_fields: List of required field names

        Raises:
            ValidationError: If any required field is missing
        """
        missing_fields = [field for field in required_fields if field not in dados]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}",
                errors={"missing_fields": missing_fields},
            )

