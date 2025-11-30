"""DCTFWEB - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsultarXmlDeclaracao38Template(BaseTemplate):
    """Template for CONSXMLDECLARACAO38 - Consultar XML da Declaração."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DCTFWEB",
            id_servico="CONSXMLDECLARACAO38",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - categoria: str (e.g., "PF_MENSAL", "GERAL_MENSAL")
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
        return "Consultar"


class ConsultarRecibo32Template(BaseTemplate):
    """Template for CONSRECIBO32 - Consultar Recibo de Transmissão."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DCTFWEB",
            id_servico="CONSRECIBO32",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - categoria: int (e.g., 40, 50)
                - anoPA: str or int (year, 4 digits)
                - mesPA: str or int (month, 1-12)
                - numeroReciboEntrega: int

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["categoria", "anoPA", "mesPA", "numeroReciboEntrega"]
        self._validate_required_fields(dados, required_fields)

        # Validate categoria - must be an integer
        categoria = dados["categoria"]
        if not isinstance(categoria, int):
            raise ValidationError("Field 'categoria' must be an integer")
        if categoria <= 0:
            raise ValidationError("Field 'categoria' must be positive")

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
            "categoria": categoria,
            "anoPA": anoPA_str,
            "mesPA": mesPA_str.zfill(2),  # Ensure 2 digits with leading zero
            "numeroReciboEntrega": numeroReciboEntrega,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ConsultarRelatorioCompleta33Template(BaseTemplate):
    """Template for CONSDECCOMPLETA33 - Consultar Relatório Declaração Completa."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="DCTFWEB",
            id_servico="CONSDECCOMPLETA33",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - categoria: str (e.g., "GERAL_MENSAL")
                - anoPA: str or int (year, 4 digits)
                - mesPA: str or int (month, 1-12)
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
            "mesPA": mesPA_str.zfill(2),  # Ensure 2 digits with leading zero
            "numeroReciboEntrega": numeroReciboEntrega,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("DCTFWEB", "CONSXMLDECLARACAO38", ConsultarXmlDeclaracao38Template)
TemplateRegistry.register("DCTFWEB", "CONSRECIBO32", ConsultarRecibo32Template)
TemplateRegistry.register("DCTFWEB", "CONSDECCOMPLETA33", ConsultarRelatorioCompleta33Template)

