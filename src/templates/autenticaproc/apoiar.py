"""AUTENTICAPROCURADOR - Apoiar templates."""

import base64
from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class EnvioXMLAssinado81Template(BaseTemplate):
    """Template for ENVIOXMLASSINADO81 - Envio de XML assinado com o Termo de Autorização."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="AUTENTICAPROCURADOR",
            id_servico="ENVIOXMLASSINADO81",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - xml: str (Base64 encoded XML string)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails

        Examples:
            >>> template = EnvioXMLAssinado81Template()
            >>> template.validate({"xml": "PHRlcm1vRGVBdXRvcml6YWNhbz4..."})
            {'xml': 'PHRlcm1vRGVBdXRvcml6YWNhbz4...'}
        """
        self._validate_required_fields(dados, ["xml"])

        xml = dados["xml"]
        if not isinstance(xml, str):
            raise ValidationError("Field 'xml' must be a string")

        if not xml.strip():
            raise ValidationError("Field 'xml' cannot be empty")

        # Validate that it's a valid base64 string
        try:
            # Try to decode to verify it's valid base64
            base64.b64decode(xml.strip(), validate=True)
        except Exception as e:
            raise ValidationError(
                f"Field 'xml' must be a valid Base64 encoded string: {str(e)}"
            )

        return {"xml": xml.strip()}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Apoiar"


# Register template
TemplateRegistry.register("AUTENTICAPROCURADOR", "ENVIOXMLASSINADO81", EnvioXMLAssinado81Template)

