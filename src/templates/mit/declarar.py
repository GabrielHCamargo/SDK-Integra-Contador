"""MIT - Declarar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class Encapuracao314Template(BaseTemplate):
    """Template for ENCAPURACAO314 - Encerrar Apuração."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="MIT",
            id_servico="ENCAPURACAO314",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - PeriodoApuracao: dict with MesApuracao (int, 1-12) and AnoApuracao (int, 1900-2100)
                - DadosIniciais: dict with various fields
                - Debitos: dict with optional Irpj, Csll, PisPasep, Cofins

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["PeriodoApuracao", "DadosIniciais"]
        self._validate_required_fields(dados, required_fields)

        # Validate PeriodoApuracao
        periodo = dados["PeriodoApuracao"]
        if not isinstance(periodo, dict):
            raise ValidationError("Field 'PeriodoApuracao' must be a dictionary")

        if "MesApuracao" not in periodo:
            raise ValidationError("Field 'PeriodoApuracao.MesApuracao' is required")
        mes = periodo["MesApuracao"]
        if isinstance(mes, str):
            try:
                mes = int(mes)
            except ValueError:
                raise ValidationError("Field 'PeriodoApuracao.MesApuracao' must be a valid integer")
        if not isinstance(mes, int) or mes < 1 or mes > 12:
            raise ValidationError("Field 'PeriodoApuracao.MesApuracao' must be between 1 and 12")

        if "AnoApuracao" not in periodo:
            raise ValidationError("Field 'PeriodoApuracao.AnoApuracao' is required")
        ano = periodo["AnoApuracao"]
        if isinstance(ano, str):
            try:
                ano = int(ano)
            except ValueError:
                raise ValidationError("Field 'PeriodoApuracao.AnoApuracao' must be a valid integer")
        if not isinstance(ano, int) or ano < 1900 or ano > 2100:
            raise ValidationError("Field 'PeriodoApuracao.AnoApuracao' must be between 1900 and 2100")

        # Validate DadosIniciais
        dados_iniciais = dados["DadosIniciais"]
        if not isinstance(dados_iniciais, dict):
            raise ValidationError("Field 'DadosIniciais' must be a dictionary")

        # Return validated data (keeping structure as-is for complex nested data)
        validated = {
            "PeriodoApuracao": {
                "MesApuracao": mes,
                "AnoApuracao": ano,
            },
            "DadosIniciais": dados_iniciais,
        }

        # Debitos is optional
        if "Debitos" in dados:
            validated["Debitos"] = dados["Debitos"]

        return validated

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Declarar"


# Register template
TemplateRegistry.register("MIT", "ENCAPURACAO314", Encapuracao314Template)

