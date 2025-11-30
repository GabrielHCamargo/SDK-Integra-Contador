"""DEFIS - Declarar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class TransDeclaracao141Template(BaseTemplate):
    """Template for TRANSDECLARACAO141 - Entregar Defis."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DEFIS",
            id_servico="TRANSDECLARACAO141",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - ano: int (year, 4 digits)
                - inatividade: int (inactivity status code)
                Optional fields:
                - situacaoEspecial: str or None
                - empresa: dict (company data structure)
                - naoOptante: dict or None

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails

        Note:
            This service accepts a complex nested structure. Only basic
            required fields are validated here. The full structure is passed
            through to the API.
        """
        # Validate required fields
        required_fields = ["ano", "inatividade"]
        self._validate_required_fields(dados, required_fields)

        # Validate ano
        ano = dados["ano"]
        if not isinstance(ano, (str, int)):
            raise ValidationError("Field 'ano' must be a string or integer")
        ano_int = int(ano)
        if not (1900 <= ano_int <= 2100):
            raise ValidationError("Field 'ano' must be a valid year (1900-2100)")

        # Validate inatividade
        inatividade = dados["inatividade"]
        if not isinstance(inatividade, (str, int)):
            raise ValidationError("Field 'inatividade' must be a string or integer")
        inatividade_int = int(inatividade)
        if inatividade_int < 0:
            raise ValidationError("Field 'inatividade' must be a non-negative integer")

        # Build validated data - preserve all fields as-is
        validated = {
            "ano": ano_int,
            "inatividade": inatividade_int,
        }

        # Add optional fields if present
        if "situacaoEspecial" in dados:
            validated["situacaoEspecial"] = dados["situacaoEspecial"]

        if "empresa" in dados:
            validated["empresa"] = dados["empresa"]

        if "naoOptante" in dados:
            validated["naoOptante"] = dados["naoOptante"]

        return validated

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Declarar"


# Register template
TemplateRegistry.register("DEFIS", "TRANSDECLARACAO141", TransDeclaracao141Template)

