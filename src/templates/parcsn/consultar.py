"""PARCSN - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class PedidosParc163Template(BaseTemplate):
    """Template for PEDIDOSPARC163 - Consultar pedidos."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PARCSN",
            id_servico="PEDIDOSPARC163",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary (must be empty)

        Returns:
            Validated data (empty dict)

        Raises:
            ValidationError: If validation fails
        """
        if dados:
            raise ValidationError("Field 'dados' must be empty for this service")
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados to JSON string.

        Args:
            dados: Validated data dictionary

        Returns:
            Empty string for this service
        """
        return ""


class ObterParc164Template(BaseTemplate):
    """Template for OBTERPARC164 - Consultar Parcelamento."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PARCSN",
            id_servico="OBTERPARC164",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - numeroParcelamento: int (parcelamento number)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["numeroParcelamento"]
        self._validate_required_fields(dados, required_fields)

        # Validate numeroParcelamento
        numero = dados["numeroParcelamento"]
        if isinstance(numero, str):
            try:
                numero = int(numero)
            except ValueError:
                raise ValidationError("Field 'numeroParcelamento' must be a valid integer")
        if not isinstance(numero, int):
            raise ValidationError("Field 'numeroParcelamento' must be an integer")
        if numero < 0:
            raise ValidationError("Field 'numeroParcelamento' must be non-negative")

        return {"numeroParcelamento": numero}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ParcelasParaGerar162Template(BaseTemplate):
    """Template for PARCELASPARAGERAR162 - Consultar Parcelas para Impressão."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PARCSN",
            id_servico="PARCELASPARAGERAR162",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary (must be empty)

        Returns:
            Validated data (empty dict)

        Raises:
            ValidationError: If validation fails
        """
        if dados:
            raise ValidationError("Field 'dados' must be empty for this service")
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados to JSON string.

        Args:
            dados: Validated data dictionary

        Returns:
            Empty string for this service
        """
        return ""


class DetPagtoParc165Template(BaseTemplate):
    """Template for DETPAGTOPARC165 - Consultar Detalhes de Pagamento."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PARCSN",
            id_servico="DETPAGTOPARC165",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - numeroParcelamento: int (parcelamento number)
                - anoMesParcela: int (year-month in format YYYYMM, e.g., 201612)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["numeroParcelamento", "anoMesParcela"]
        self._validate_required_fields(dados, required_fields)

        # Validate numeroParcelamento
        numero = dados["numeroParcelamento"]
        if isinstance(numero, str):
            try:
                numero = int(numero)
            except ValueError:
                raise ValidationError("Field 'numeroParcelamento' must be a valid integer")
        if not isinstance(numero, int):
            raise ValidationError("Field 'numeroParcelamento' must be an integer")
        if numero < 0:
            raise ValidationError("Field 'numeroParcelamento' must be non-negative")

        # Validate anoMesParcela
        ano_mes = dados["anoMesParcela"]
        if isinstance(ano_mes, str):
            try:
                ano_mes = int(ano_mes)
            except ValueError:
                raise ValidationError("Field 'anoMesParcela' must be a valid integer")
        if not isinstance(ano_mes, int):
            raise ValidationError("Field 'anoMesParcela' must be an integer")
        # Validate format YYYYMM (e.g., 201612 = December 2016)
        if ano_mes < 190000 or ano_mes > 210012:
            raise ValidationError("Field 'anoMesParcela' must be in YYYYMM format (e.g., 201612)")

        return {
            "numeroParcelamento": numero,
            "anoMesParcela": ano_mes,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("PARCSN", "PEDIDOSPARC163", PedidosParc163Template)
TemplateRegistry.register("PARCSN", "OBTERPARC164", ObterParc164Template)
TemplateRegistry.register("PARCSN", "PARCELASPARAGERAR162", ParcelasParaGerar162Template)
TemplateRegistry.register("PARCSN", "DETPAGTOPARC165", DetPagtoParc165Template)

