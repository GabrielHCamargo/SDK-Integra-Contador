"""PGDAS-D - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsDeclaracao13Template(BaseTemplate):
    """Template for CONSDECLARACAO13 - Consultar Declarações Transmitidas por Ano-Calendário ou Período de Apuração."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="CONSDECLARACAO13",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - anoCalendario: str (year in format YYYY, e.g., "2018")

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
        # Validate format YYYY (e.g., "2018")
        if len(ano) != 4 or not ano.isdigit():
            raise ValidationError("Field 'anoCalendario' must be in YYYY format (e.g., '2018')")
        ano_int = int(ano)
        if ano_int < 1900 or ano_int > 2100:
            raise ValidationError("Field 'anoCalendario' must be a valid year between 1900 and 2100")

        return {"anoCalendario": ano}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ConsultimaDecRec14Template(BaseTemplate):
    """Template for CONSULTIMADECREC14 - Consultar a Última Declaração/Recibo."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="CONSULTIMADECREC14",
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
        return "Consultar"


class ConsDecRec15Template(BaseTemplate):
    """Template for CONSDECREC15 - Consultar Declaração/Recibo."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="CONSDECREC15",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - numeroDeclaracao: str (declaration number)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["numeroDeclaracao"]
        self._validate_required_fields(dados, required_fields)

        # Validate numeroDeclaracao
        numero = dados["numeroDeclaracao"]
        if isinstance(numero, int):
            numero = str(numero)
        if not isinstance(numero, str):
            raise ValidationError("Field 'numeroDeclaracao' must be a string")
        if not numero.strip():
            raise ValidationError("Field 'numeroDeclaracao' cannot be empty")

        return {"numeroDeclaracao": numero}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ConsExtrato16Template(BaseTemplate):
    """Template for CONSEXTRATO16 - Consultar Extrato do DAS."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PGDASD",
            id_servico="CONSEXTRATO16",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - numeroDas: str (DAS number)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["numeroDas"]
        self._validate_required_fields(dados, required_fields)

        # Validate numeroDas
        numero = dados["numeroDas"]
        if isinstance(numero, int):
            numero = str(numero)
        if not isinstance(numero, str):
            raise ValidationError("Field 'numeroDas' must be a string")
        if not numero.strip():
            raise ValidationError("Field 'numeroDas' cannot be empty")

        return {"numeroDas": numero}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("PGDASD", "CONSDECLARACAO13", ConsDeclaracao13Template)
TemplateRegistry.register("PGDASD", "CONSULTIMADECREC14", ConsultimaDecRec14Template)
TemplateRegistry.register("PGDASD", "CONSDECREC15", ConsDecRec15Template)
TemplateRegistry.register("PGDASD", "CONSEXTRATO16", ConsExtrato16Template)


