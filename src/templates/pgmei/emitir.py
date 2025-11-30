"""PGMEI - Emitir templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class GerardasPdf21Template(BaseTemplate):
    """Template for GERARDASPDF21 - Gerar DAS."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGMEI",
            id_servico="GERARDASPDF21",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - periodoApuracao: str (period in format YYYYMM, e.g., "201901")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["periodoApuracao"]
        self._validate_required_fields(dados, required_fields)

        # Validate periodoApuracao
        periodo = dados["periodoApuracao"]
        if isinstance(periodo, int):
            periodo = str(periodo)
        if not isinstance(periodo, str):
            raise ValidationError("Field 'periodoApuracao' must be a string")
        # Validate format YYYYMM (e.g., "201901")
        if len(periodo) != 6 or not periodo.isdigit():
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '201901')")
        periodo_int = int(periodo)
        if periodo_int < 190000 or periodo_int > 210012:
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '201901')")

        return {"periodoApuracao": periodo}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


class GerardasCodBarra22Template(BaseTemplate):
    """Template for GERARDASCODBARRA22 - Gerar DAS Código de Barras."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGMEI",
            id_servico="GERARDASCODBARRA22",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - periodoApuracao: str (period in format YYYYMM, e.g., "201901")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["periodoApuracao"]
        self._validate_required_fields(dados, required_fields)

        # Validate periodoApuracao
        periodo = dados["periodoApuracao"]
        if isinstance(periodo, int):
            periodo = str(periodo)
        if not isinstance(periodo, str):
            raise ValidationError("Field 'periodoApuracao' must be a string")
        # Validate format YYYYMM (e.g., "201901")
        if len(periodo) != 6 or not periodo.isdigit():
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '201901')")
        periodo_int = int(periodo)
        if periodo_int < 190000 or periodo_int > 210012:
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '201901')")

        return {"periodoApuracao": periodo}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


class AtuBeneficio23Template(BaseTemplate):
    """Template for ATUBENEFICIO23 - Atualizar Benefício."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGMEI",
            id_servico="ATUBENEFICIO23",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - anoCalendario: int (year, e.g., 2021)
                - infoBeneficio: list (list of benefit info objects)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["anoCalendario", "infoBeneficio"]
        self._validate_required_fields(dados, required_fields)

        # Validate anoCalendario
        ano = dados["anoCalendario"]
        if isinstance(ano, str):
            try:
                ano = int(ano)
            except ValueError:
                raise ValidationError("Field 'anoCalendario' must be a valid integer")
        if not isinstance(ano, int):
            raise ValidationError("Field 'anoCalendario' must be an integer")
        if ano < 1900 or ano > 2100:
            raise ValidationError("Field 'anoCalendario' must be a valid year between 1900 and 2100")

        # Validate infoBeneficio
        info = dados["infoBeneficio"]
        if not isinstance(info, list):
            raise ValidationError("Field 'infoBeneficio' must be a list")
        if not info:
            raise ValidationError("Field 'infoBeneficio' cannot be empty")

        return {
            "anoCalendario": ano,
            "infoBeneficio": info,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register templates
TemplateRegistry.register("PGMEI", "GERARDASPDF21", GerardasPdf21Template)
TemplateRegistry.register("PGMEI", "GERARDASCODBARRA22", GerardasCodBarra22Template)
TemplateRegistry.register("PGMEI", "ATUBENEFICIO23", AtuBeneficio23Template)


