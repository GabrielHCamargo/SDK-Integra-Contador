"""PERTSN - Emitir templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class Gerardas181Template(BaseTemplate):
    """Template for GERARDAS181 - Emitir DAS."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PERTSN",
            id_servico="GERARDAS181",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - parcelaParaEmitir: int (parcela to emit in format YYYYMM, e.g., 202301)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["parcelaParaEmitir"]
        self._validate_required_fields(dados, required_fields)

        # Validate parcelaParaEmitir
        parcela = dados["parcelaParaEmitir"]
        if isinstance(parcela, str):
            try:
                parcela = int(parcela)
            except ValueError:
                raise ValidationError("Field 'parcelaParaEmitir' must be a valid integer")
        if not isinstance(parcela, int):
            raise ValidationError("Field 'parcelaParaEmitir' must be an integer")
        # Validate format YYYYMM (e.g., 202301 = January 2023)
        if parcela < 190000 or parcela > 210012:
            raise ValidationError("Field 'parcelaParaEmitir' must be in YYYYMM format (e.g., 202301)")

        return {"parcelaParaEmitir": parcela}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register template
TemplateRegistry.register("PERTSN", "GERARDAS181", Gerardas181Template)

