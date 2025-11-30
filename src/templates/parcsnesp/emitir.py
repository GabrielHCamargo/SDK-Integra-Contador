"""PARCSN-ESP - Emitir templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class Gerardas171Template(BaseTemplate):
    """Template for GERARDAS171 - Emitir DAS."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PARCSN-ESP",
            id_servico="GERARDAS171",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - parcelaParaEmitir: int (parcela to emit in format YYYYMM, e.g., 202306)

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
        # Validate format YYYYMM (e.g., 202306 = June 2023)
        if parcela < 190000 or parcela > 210012:
            raise ValidationError("Field 'parcelaParaEmitir' must be in YYYYMM format (e.g., 202306)")

        return {"parcelaParaEmitir": parcela}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register template
TemplateRegistry.register("PARCSN-ESP", "GERARDAS171", Gerardas171Template)

