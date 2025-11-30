"""SITFIS - Emitir templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class RelatorioSitfis92Template(BaseTemplate):
    """Template for RELATORIOSITFIS92 - Emitir Relatório de Situação Fiscal."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="SITFIS",
            id_servico="RELATORIOSITFIS92",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - protocoloRelatorio: str (protocol number from previous request)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["protocoloRelatorio"]
        self._validate_required_fields(dados, required_fields)

        # Validate protocoloRelatorio
        if not isinstance(dados["protocoloRelatorio"], str):
            raise ValidationError("Field 'protocoloRelatorio' must be a string")
        if not dados["protocoloRelatorio"]:
            raise ValidationError("Field 'protocoloRelatorio' cannot be empty")

        return dados

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register template
TemplateRegistry.register("SITFIS", "RELATORIOSITFIS92", RelatorioSitfis92Template)


