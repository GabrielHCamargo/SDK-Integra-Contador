"""PAGTOWEB - Emitir templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class Comparrecadacao72Template(BaseTemplate):
    """Template for COMPARRECADACAO72 - Emitir Comprovante de Pagamento."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PAGTOWEB",
            id_servico="COMPARRECADACAO72",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - numeroDocumento: str (document number)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["numeroDocumento"]
        self._validate_required_fields(dados, required_fields)

        # Validate numeroDocumento
        numero_documento = dados["numeroDocumento"]
        if not isinstance(numero_documento, str):
            raise ValidationError("Field 'numeroDocumento' must be a string")
        if not numero_documento.strip():
            raise ValidationError("Field 'numeroDocumento' cannot be empty")

        return {"numeroDocumento": numero_documento.strip()}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register template
TemplateRegistry.register("PAGTOWEB", "COMPARRECADACAO72", Comparrecadacao72Template)

