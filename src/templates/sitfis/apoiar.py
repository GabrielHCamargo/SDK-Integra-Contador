"""SITFIS - Apoiar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class SolicitarProtocolo91Template(BaseTemplate):
    """Template for SOLICITARPROTOCOLO91 - Solicitar protocolo do relatório de situação fiscal."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="SITFIS",
            id_servico="SOLICITARPROTOCOLO91",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary (must be empty)

        Returns:
            Validated data (empty dict)

        Raises:
            ValidationError: If validation fails
        """
        if dados:
            raise ValidationError("Field 'dados' must be empty for this service")
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Apoiar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados to JSON string.

        Args:
            dados: Validated data dictionary

        Returns:
            Empty string for this service
        """
        return ""


# Register template
TemplateRegistry.register("SITFIS", "SOLICITARPROTOCOLO91", SolicitarProtocolo91Template)


