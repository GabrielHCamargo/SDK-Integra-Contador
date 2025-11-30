"""DCTFWEB - Transmitir templates."""

import base64
from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class TransmitirDeclaracao310Template(BaseTemplate):
    """Template for TRANSDECLARACAO310 - Transmitir Declaração."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DCTFWEB",
            id_servico="TRANSDECLARACAO310",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - categoria: str (e.g., "PF_MENSAL")
                - anoPA: str or int (year, 4 digits)
                - mesPA: str or int (month, 1-12)
                - xmlAssinadoBase64: str (Base64 encoded signed XML string)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["categoria", "anoPA", "mesPA", "xmlAssinadoBase64"]
        self._validate_required_fields(dados, required_fields)

        # Validate categoria
        categoria = dados["categoria"]
        if not isinstance(categoria, str):
            raise ValidationError("Field 'categoria' must be a string")
        if not categoria.strip():
            raise ValidationError("Field 'categoria' cannot be empty")

        # Validate anoPA
        anoPA = dados["anoPA"]
        if not isinstance(anoPA, (str, int)):
            raise ValidationError("Field 'anoPA' must be a string or integer")
        anoPA_str = str(anoPA).strip()
        if not anoPA_str.isdigit() or len(anoPA_str) != 4:
            raise ValidationError("Field 'anoPA' must be a 4-digit year")

        # Validate mesPA
        mesPA = dados["mesPA"]
        if not isinstance(mesPA, (str, int)):
            raise ValidationError("Field 'mesPA' must be a string or integer")
        mesPA_str = str(mesPA).strip()
        if not mesPA_str.isdigit() or not (1 <= int(mesPA_str) <= 12):
            raise ValidationError("Field 'mesPA' must be a valid month (1-12)")

        # Validate xmlAssinadoBase64
        xmlAssinadoBase64 = dados["xmlAssinadoBase64"]
        if not isinstance(xmlAssinadoBase64, str):
            raise ValidationError("Field 'xmlAssinadoBase64' must be a string")
        if not xmlAssinadoBase64.strip():
            raise ValidationError("Field 'xmlAssinadoBase64' cannot be empty")

        # Validate that it's a valid base64 string
        try:
            base64.b64decode(xmlAssinadoBase64.strip(), validate=True)
        except Exception as e:
            raise ValidationError(
                f"Field 'xmlAssinadoBase64' must be a valid Base64 encoded string: {str(e)}"
            )

        return {
            "categoria": categoria.strip(),
            "anoPA": anoPA_str,
            "mesPA": mesPA_str.zfill(2),  # Ensure 2 digits with leading zero
            "xmlAssinadoBase64": xmlAssinadoBase64.strip(),
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Transmitir"


# Register template
TemplateRegistry.register("DCTFWEB", "TRANSDECLARACAO310", TransmitirDeclaracao310Template)

