"""PGMEI - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsDividaAtiva24Template(BaseTemplate):
    """Template for DIVIDAATIVA24 - Consultar Dívida Ativa."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGMEI",
            id_servico="DIVIDAATIVA24",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - anoCalendario: str (year in format YYYY, e.g., "2020")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["anoCalendario"]
        self._validate_required_fields(dados, required_fields)

        # Validate anoCalendario
        ano = dados["anoCalendario"]
        if isinstance(ano, int):
            ano = str(ano)
        if not isinstance(ano, str):
            raise ValidationError("Field 'anoCalendario' must be a string")
        # Validate format YYYY (e.g., "2020")
        if len(ano) != 4 or not ano.isdigit():
            raise ValidationError("Field 'anoCalendario' must be in YYYY format (e.g., '2020')")
        ano_int = int(ano)
        if ano_int < 1900 or ano_int > 2100:
            raise ValidationError("Field 'anoCalendario' must be a valid year between 1900 and 2100")

        return {"anoCalendario": ano}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register template
TemplateRegistry.register("PGMEI", "DIVIDAATIVA24", ConsDividaAtiva24Template)

