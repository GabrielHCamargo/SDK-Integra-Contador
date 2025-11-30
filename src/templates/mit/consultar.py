"""MIT - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsApuracao316Template(BaseTemplate):
    """Template for CONSAPURACAO316 - Consultar Apuração."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="MIT",
            id_servico="CONSAPURACAO316",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - IdApuracao: int (apuração ID)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["IdApuracao"]
        self._validate_required_fields(dados, required_fields)

        # Validate IdApuracao
        id_apuracao = dados["IdApuracao"]
        if isinstance(id_apuracao, str):
            try:
                id_apuracao = int(id_apuracao)
            except ValueError:
                raise ValidationError("Field 'IdApuracao' must be a valid integer")
        if not isinstance(id_apuracao, int):
            raise ValidationError("Field 'IdApuracao' must be an integer")
        if id_apuracao < 0:
            raise ValidationError("Field 'IdApuracao' must be non-negative")

        return {"IdApuracao": id_apuracao}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ListaApuracoes317Template(BaseTemplate):
    """Template for LISTAAPURACOES317 - Listar Apuração por mês e ano."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="MIT",
            id_servico="LISTAAPURACOES317",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - mesApuracao: int (1-12)
                - anoApuracao: int (1900-2100)
                - situacaoApuracao: int (situation code)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["mesApuracao", "anoApuracao", "situacaoApuracao"]
        self._validate_required_fields(dados, required_fields)

        # Validate mesApuracao
        mes = dados["mesApuracao"]
        if isinstance(mes, str):
            try:
                mes = int(mes)
            except ValueError:
                raise ValidationError("Field 'mesApuracao' must be a valid integer")
        if not isinstance(mes, int) or mes < 1 or mes > 12:
            raise ValidationError("Field 'mesApuracao' must be between 1 and 12")

        # Validate anoApuracao
        ano = dados["anoApuracao"]
        if isinstance(ano, str):
            try:
                ano = int(ano)
            except ValueError:
                raise ValidationError("Field 'anoApuracao' must be a valid integer")
        if not isinstance(ano, int) or ano < 1900 or ano > 2100:
            raise ValidationError("Field 'anoApuracao' must be between 1900 and 2100")

        # Validate situacaoApuracao
        situacao = dados["situacaoApuracao"]
        if isinstance(situacao, str):
            try:
                situacao = int(situacao)
            except ValueError:
                raise ValidationError("Field 'situacaoApuracao' must be a valid integer")
        if not isinstance(situacao, int):
            raise ValidationError("Field 'situacaoApuracao' must be an integer")

        return {
            "mesApuracao": mes,
            "anoApuracao": ano,
            "situacaoApuracao": situacao,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("MIT", "CONSAPURACAO316", ConsApuracao316Template)
TemplateRegistry.register("MIT", "LISTAAPURACOES317", ListaApuracoes317Template)

