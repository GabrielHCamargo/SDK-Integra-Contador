"""REGIME APURACAO - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsultarAnosCalendarios102Template(BaseTemplate):
    """Template for CONSULTARANOSCALENDARIOS102 - Consultar Anos Calendários."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="REGIMEAPURACAO",
            id_servico="CONSULTARANOSCALENDARIOS102",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary (must be empty)

        Returns:
            Validated data (empty dict)

        Raises:
            ValidationError: If validation fails
        """
        if dados:
            raise ValidationError("Field 'dados' must be empty for this service")
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados to JSON string.

        Args:
            dados: Validated data dictionary

        Returns:
            Empty string for this service
        """
        return ""


class ConsultarOpcaoRegime103Template(BaseTemplate):
    """Template for CONSULTAROPCAOREGIME103 - Consultar opção Regime."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="REGIMEAPURACAO",
            id_servico="CONSULTAROPCAOREGIME103",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - anoCalendario: int (year, e.g., 2023)

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
        if isinstance(ano, str):
            try:
                ano = int(ano)
            except ValueError:
                raise ValidationError("Field 'anoCalendario' must be a valid integer")
        if not isinstance(ano, int):
            raise ValidationError("Field 'anoCalendario' must be an integer")
        if ano < 1900 or ano > 2100:
            raise ValidationError("Field 'anoCalendario' must be a valid year between 1900 and 2100")

        return {"anoCalendario": ano}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ConsultarResolucao104Template(BaseTemplate):
    """Template for CONSULTARRESOLUCAO104 - Consultar Resolução."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="REGIMEAPURACAO",
            id_servico="CONSULTARRESOLUCAO104",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - anoCalendario: int (year, e.g., 2021)

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
        if isinstance(ano, str):
            try:
                ano = int(ano)
            except ValueError:
                raise ValidationError("Field 'anoCalendario' must be a valid integer")
        if not isinstance(ano, int):
            raise ValidationError("Field 'anoCalendario' must be an integer")
        if ano < 1900 or ano > 2100:
            raise ValidationError("Field 'anoCalendario' must be a valid year between 1900 and 2100")

        return {"anoCalendario": ano}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("REGIMEAPURACAO", "CONSULTARANOSCALENDARIOS102", ConsultarAnosCalendarios102Template)
TemplateRegistry.register("REGIMEAPURACAO", "CONSULTAROPCAOREGIME103", ConsultarOpcaoRegime103Template)
TemplateRegistry.register("REGIMEAPURACAO", "CONSULTARRESOLUCAO104", ConsultarResolucao104Template)


