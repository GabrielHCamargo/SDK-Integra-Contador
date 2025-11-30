"""PGDAS-D - Emitir templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class Gerardas12Template(BaseTemplate):
    """Template for GERARDAS12 - Gerar DAS."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="GERARDAS12",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - periodoApuracao: str (period in format YYYYMM, e.g., "201801")

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
        # Validate format YYYYMM (e.g., "201801")
        if len(periodo) != 6 or not periodo.isdigit():
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '201801')")
        periodo_int = int(periodo)
        if periodo_int < 190000 or periodo_int > 210012:
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '201801')")

        return {"periodoApuracao": periodo}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


class GerardasAvulso19Template(BaseTemplate):
    """Template for GERARDASAVULSO19 - Gerar DAS Avulso."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="GERARDASAVULSO19",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - PeriodoApuracao: int (period in format YYYYMM, e.g., 202401)
                - ListaTributos: list (list of tax objects)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["PeriodoApuracao", "ListaTributos"]
        self._validate_required_fields(dados, required_fields)

        # Validate PeriodoApuracao
        periodo = dados["PeriodoApuracao"]
        if isinstance(periodo, str):
            try:
                periodo = int(periodo)
            except ValueError:
                raise ValidationError("Field 'PeriodoApuracao' must be a valid integer")
        if not isinstance(periodo, int):
            raise ValidationError("Field 'PeriodoApuracao' must be an integer")
        # Validate format YYYYMM (e.g., 202401)
        if periodo < 190000 or periodo > 210012:
            raise ValidationError("Field 'PeriodoApuracao' must be in YYYYMM format (e.g., 202401)")

        # Validate ListaTributos
        lista = dados["ListaTributos"]
        if not isinstance(lista, list):
            raise ValidationError("Field 'ListaTributos' must be a list")
        if not lista:
            raise ValidationError("Field 'ListaTributos' cannot be empty")

        return {
            "PeriodoApuracao": periodo,
            "ListaTributos": lista,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


class GerardasCobranca17Template(BaseTemplate):
    """Template for GERARDASCOBRANCA17 - Gerar DAS Cobrança."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="GERARDASCOBRANCA17",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - periodoApuracao: str (period in format YYYYMM, e.g., "202301")

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
        # Validate format YYYYMM (e.g., "202301")
        if len(periodo) != 6 or not periodo.isdigit():
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '202301')")
        periodo_int = int(periodo)
        if periodo_int < 190000 or periodo_int > 210012:
            raise ValidationError("Field 'periodoApuracao' must be in YYYYMM format (e.g., '202301')")

        return {"periodoApuracao": periodo}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


class GerardasProcesso18Template(BaseTemplate):
    """Template for GERARDASPROCESSO18 - Gerar DAS de Processo."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="GERARDASPROCESSO18",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - numeroProcesso: str (process number)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["numeroProcesso"]
        self._validate_required_fields(dados, required_fields)

        # Validate numeroProcesso
        numero = dados["numeroProcesso"]
        if isinstance(numero, int):
            numero = str(numero)
        if not isinstance(numero, str):
            raise ValidationError("Field 'numeroProcesso' must be a string")
        if not numero.strip():
            raise ValidationError("Field 'numeroProcesso' cannot be empty")

        return {"numeroProcesso": numero}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register templates
TemplateRegistry.register("PGDASD", "GERARDAS12", Gerardas12Template)
TemplateRegistry.register("PGDASD", "GERARDASAVULSO19", GerardasAvulso19Template)
TemplateRegistry.register("PGDASD", "GERARDASCOBRANCA17", GerardasCobranca17Template)
TemplateRegistry.register("PGDASD", "GERARDASPROCESSO18", GerardasProcesso18Template)


