"""PGDAS-D - Declarar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class TransDeclaracao11Template(BaseTemplate):
    """Template for TRANSDECLARACAO11 - Entregar Declaração."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="TRANSDECLARACAO11",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with complex structure for declaration submission.
                   This service accepts a complex JSON structure that will be validated
                   minimally to ensure it's a non-empty dictionary.

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Basic validation - ensure dados is a dict and not empty
        if not isinstance(dados, dict):
            raise ValidationError("Field 'dados' must be a dictionary")
        if not dados:
            raise ValidationError("Field 'dados' cannot be empty")

        # Return dados as-is since it's a complex structure
        # The API will validate the full structure
        return dados

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Declarar"


# Register template
TemplateRegistry.register("PGDASD", "TRANSDECLARACAO11", TransDeclaracao11Template)


