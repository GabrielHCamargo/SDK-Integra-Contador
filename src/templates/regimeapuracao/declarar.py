"""REGIME APURACAO - Declarar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class EfetuarOpcaoRegime101Template(BaseTemplate):
    """Template for EFETUAROPCAOREGIME101 - Efetuar opção."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="REGIMEAPURACAO",
            id_servico="EFETUAROPCAOREGIME101",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - anoOpcao: int (year of option, e.g., 2023)
                - tipoRegime: int (regime type)
                - descritivoRegime: str (regime description, e.g., "CAIXA")
                - deAcordoResolucao: bool (according to resolution)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["anoOpcao", "tipoRegime", "descritivoRegime", "deAcordoResolucao"]
        self._validate_required_fields(dados, required_fields)

        # Validate anoOpcao
        ano = dados["anoOpcao"]
        if isinstance(ano, str):
            try:
                ano = int(ano)
            except ValueError:
                raise ValidationError("Field 'anoOpcao' must be a valid integer")
        if not isinstance(ano, int):
            raise ValidationError("Field 'anoOpcao' must be an integer")
        if ano < 1900 or ano > 2100:
            raise ValidationError("Field 'anoOpcao' must be a valid year between 1900 and 2100")

        # Validate tipoRegime
        tipo = dados["tipoRegime"]
        if isinstance(tipo, str):
            try:
                tipo = int(tipo)
            except ValueError:
                raise ValidationError("Field 'tipoRegime' must be a valid integer")
        if not isinstance(tipo, int):
            raise ValidationError("Field 'tipoRegime' must be an integer")

        # Validate descritivoRegime
        descritivo = dados["descritivoRegime"]
        if isinstance(descritivo, int):
            descritivo = str(descritivo)
        if not isinstance(descritivo, str):
            raise ValidationError("Field 'descritivoRegime' must be a string")
        if not descritivo.strip():
            raise ValidationError("Field 'descritivoRegime' cannot be empty")

        # Validate deAcordoResolucao
        acordo = dados["deAcordoResolucao"]
        if isinstance(acordo, str):
            acordo = acordo.lower() in ("true", "1", "yes")
        if not isinstance(acordo, bool):
            raise ValidationError("Field 'deAcordoResolucao' must be a boolean")

        return {
            "anoOpcao": ano,
            "tipoRegime": tipo,
            "descritivoRegime": descritivo,
            "deAcordoResolucao": acordo,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Declarar"


# Register template
TemplateRegistry.register("REGIMEAPURACAO", "EFETUAROPCAOREGIME101", EfetuarOpcaoRegime101Template)


