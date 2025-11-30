"""DTE - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsultaSituacaoDte111Template(BaseTemplate):
    """Template for CONSULTASITUACAODTE111 - Obter indicador DTE."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DTE",
            id_servico="CONSULTASITUACAODTE111",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary. This service requires empty dados.

        Returns:
            Validated data (empty dict)

        Raises:
            ValidationError: If validation fails

        Note:
            This service does not require any input data. The dados field
            should be empty or contain only empty/whitespace strings.
        """
        # This service requires empty dados
        if dados:
            # Check if all values are empty/whitespace
            non_empty = {
                k: v for k, v in dados.items() if v and str(v).strip()
            }
            if non_empty:
                raise ValidationError(
                    "This service does not accept input data. "
                    "The 'dados' field must be empty."
                )

        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados to JSON string.

        Args:
            dados: Data dictionary

        Returns:
            Empty string for this service
        """
        return ""


# Register template
TemplateRegistry.register("DTE", "CONSULTASITUACAODTE111", ConsultaSituacaoDte111Template)

