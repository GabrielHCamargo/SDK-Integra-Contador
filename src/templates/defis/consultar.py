"""DEFIS - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsDeclaracao142Template(BaseTemplate):
    """Template for CONSDECLARACAO142 - Consultar Declarações."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DEFIS",
            id_servico="CONSDECLARACAO142",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary. This service requires empty dados.

        Returns:
            Validated data (empty dict)

        Raises:
            ValidationError: If validation fails

        Note:
            This service does not require any input data. The dados field
            should be empty or contain only empty/whitespace strings.
        """
        # This service requires empty dados
        if dados:
            # Check if all values are empty/whitespace
            non_empty = {
                k: v for k, v in dados.items() if v and str(v).strip()
            }
            if non_empty:
                raise ValidationError(
                    "This service does not accept input data. "
                    "The 'dados' field must be empty."
                )

        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados to JSON string.

        Args:
            dados: Data dictionary

        Returns:
            Empty string for this service
        """
        return ""


class ConsUltimaDecRec143Template(BaseTemplate):
    """Template for CONSULTIMADECREC143 - Consultar Última Declaração e Recibo."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DEFIS",
            id_servico="CONSULTIMADECREC143",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - ano: int (year, 4 digits)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["ano"]
        self._validate_required_fields(dados, required_fields)

        # Validate ano
        ano = dados["ano"]
        if not isinstance(ano, (str, int)):
            raise ValidationError("Field 'ano' must be a string or integer")
        ano_int = int(ano)
        if not (1900 <= ano_int <= 2100):
            raise ValidationError("Field 'ano' must be a valid year (1900-2100)")

        return {"ano": ano_int}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ConsDecRec144Template(BaseTemplate):
    """Template for CONSDECREC144 - Consultar Declaração e Recibo."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DEFIS",
            id_servico="CONSDECREC144",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - idDefis: str (DEFIS declaration ID)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["idDefis"]
        self._validate_required_fields(dados, required_fields)

        # Validate idDefis
        id_defis = dados["idDefis"]
        if not isinstance(id_defis, str):
            raise ValidationError("Field 'idDefis' must be a string")
        if not id_defis.strip():
            raise ValidationError("Field 'idDefis' cannot be empty")

        return {"idDefis": id_defis.strip()}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("DEFIS", "CONSDECLARACAO142", ConsDeclaracao142Template)
TemplateRegistry.register("DEFIS", "CONSULTIMADECREC143", ConsUltimaDecRec143Template)
TemplateRegistry.register("DEFIS", "CONSDECREC144", ConsDecRec144Template)

