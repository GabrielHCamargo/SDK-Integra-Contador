"""PROCURACOES - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ObterProcuracao41Template(BaseTemplate):
    """Template for OBTERPROCURACAO41 - Obter Procurações."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PROCURACOES",
            id_servico="OBTERPROCURACAO41",
            versao_sistema="1",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - outorgante: str (grantor number)
                - tipoOutorgante: str (grantor type: "1" for CPF, "2" for CNPJ)
                - outorgado: str (grantee number)
                - tipoOutorgado: str (grantee type: "1" for CPF, "2" for CNPJ)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["outorgante", "tipoOutorgante", "outorgado", "tipoOutorgado"]
        self._validate_required_fields(dados, required_fields)

        # Validate outorgante
        outorgante = dados["outorgante"]
        if isinstance(outorgante, int):
            outorgante = str(outorgante)
        if not isinstance(outorgante, str):
            raise ValidationError("Field 'outorgante' must be a string")
        if not outorgante.strip():
            raise ValidationError("Field 'outorgante' cannot be empty")

        # Validate tipoOutorgante
        tipo_outorgante = dados["tipoOutorgante"]
        if isinstance(tipo_outorgante, int):
            tipo_outorgante = str(tipo_outorgante)
        if not isinstance(tipo_outorgante, str):
            raise ValidationError("Field 'tipoOutorgante' must be a string")
        if tipo_outorgante not in ["1", "2"]:
            raise ValidationError("Field 'tipoOutorgante' must be '1' (CPF) or '2' (CNPJ)")

        # Validate outorgado
        outorgado = dados["outorgado"]
        if isinstance(outorgado, int):
            outorgado = str(outorgado)
        if not isinstance(outorgado, str):
            raise ValidationError("Field 'outorgado' must be a string")
        if not outorgado.strip():
            raise ValidationError("Field 'outorgado' cannot be empty")

        # Validate tipoOutorgado
        tipo_outorgado = dados["tipoOutorgado"]
        if isinstance(tipo_outorgado, int):
            tipo_outorgado = str(tipo_outorgado)
        if not isinstance(tipo_outorgado, str):
            raise ValidationError("Field 'tipoOutorgado' must be a string")
        if tipo_outorgado not in ["1", "2"]:
            raise ValidationError("Field 'tipoOutorgado' must be '1' (CPF) or '2' (CNPJ)")

        return {
            "outorgante": outorgante,
            "tipoOutorgante": tipo_outorgante,
            "outorgado": outorgado,
            "tipoOutorgado": tipo_outorgado,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register template
TemplateRegistry.register("PROCURACOES", "OBTERPROCURACAO41", ObterProcuracao41Template)


