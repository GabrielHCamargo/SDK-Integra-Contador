"""MIT - Apoiar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class SituacaoEnc315Template(BaseTemplate):
    """Template for SITUACAOENC315 - Consulta a situação do encerramento."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="MIT",
            id_servico="SITUACAOENC315",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - protocoloEncerramento: str (protocol ID from encerramento)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["protocoloEncerramento"]
        self._validate_required_fields(dados, required_fields)

        # Validate protocoloEncerramento
        protocolo = dados["protocoloEncerramento"]
        if not isinstance(protocolo, str):
            raise ValidationError("Field 'protocoloEncerramento' must be a string")
        if not protocolo.strip():
            raise ValidationError("Field 'protocoloEncerramento' cannot be empty")

        return {"protocoloEncerramento": protocolo.strip()}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Apoiar"


# Register template
TemplateRegistry.register("MIT", "SITUACAOENC315", SituacaoEnc315Template)

