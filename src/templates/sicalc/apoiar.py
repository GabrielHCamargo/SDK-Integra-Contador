"""SICALC - Apoiar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsultaApoioReceitas52Template(BaseTemplate):
    """Template for CONSULTAAPOIORECEITAS52 - Consultar Receitas do SICALC."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="SICALC",
            id_servico="CONSULTAAPOIORECEITAS52",
            versao_sistema="2.9",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - codigoReceita: str (receita code, e.g., "6106")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["codigoReceita"]
        self._validate_required_fields(dados, required_fields)

        # Validate codigoReceita
        if not isinstance(dados["codigoReceita"], str):
            raise ValidationError("Field 'codigoReceita' must be a string")
        if not dados["codigoReceita"]:
            raise ValidationError("Field 'codigoReceita' cannot be empty")

        return dados

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Apoiar"


# Register template
TemplateRegistry.register("SICALC", "CONSULTAAPOIORECEITAS52", ConsultaApoioReceitas52Template)


