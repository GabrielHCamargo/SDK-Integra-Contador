"""DCTFWEB - Emitir templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class GerarGuia31Template(BaseTemplate):
    """Template for GERARGUIA31 - Gerar Documento de Arrecadação."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DCTFWEB",
            id_servico="GERARGUIA31",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - categoria: str (e.g., "GERAL_MENSAL")
                - anoPA: str (year)
                - mesPA: str (month)
                - numeroReciboEntrega: int

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["categoria", "anoPA", "mesPA", "numeroReciboEntrega"]
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

        # Validate numeroReciboEntrega
        numeroReciboEntrega = dados["numeroReciboEntrega"]
        if not isinstance(numeroReciboEntrega, int):
            raise ValidationError("Field 'numeroReciboEntrega' must be an integer")
        if numeroReciboEntrega <= 0:
            raise ValidationError("Field 'numeroReciboEntrega' must be positive")

        return {
            "categoria": categoria.strip(),
            "anoPA": anoPA_str,
            "mesPA": mesPA_str,
            "numeroReciboEntrega": numeroReciboEntrega,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


class GerarGuiaAndamento313Template(BaseTemplate):
    """Template for GERARGUIAANDAMENTO313 - Gerar Guia em Andamento."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DCTFWEB",
            id_servico="GERARGUIAANDAMENTO313",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - categoria: str (e.g., "GERAL_MENSAL")
                - anoPA: str or int (year, 4 digits)
                - mesPA: str or int (month, 1-12)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["categoria", "anoPA", "mesPA"]
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

        return {
            "categoria": categoria.strip(),
            "anoPA": anoPA_str,
            "mesPA": mesPA_str.zfill(2),  # Ensure 2 digits with leading zero
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register templates
TemplateRegistry.register("DCTFWEB", "GERARGUIA31", GerarGuia31Template)
TemplateRegistry.register("DCTFWEB", "GERARGUIAANDAMENTO313", GerarGuiaAndamento313Template)

