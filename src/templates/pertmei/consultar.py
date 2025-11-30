"""PERTMEI - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class PedidosParc223Template(BaseTemplate):
    """Template for PEDIDOSPARC223 - Consultar pedidos."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PERTMEI",
            id_servico="PEDIDOSPARC223",
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


class ObterParc224Template(BaseTemplate):
    """Template for OBTERPARC224 - Consultar Parcelamento."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PERTMEI",
            id_servico="OBTERPARC224",
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


class ParcelasParaGerar222Template(BaseTemplate):
    """Template for PARCELASPARAGERAR222 - Consultar Parcelas para Impressão."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PERTMEI",
            id_servico="PARCELASPARAGERAR222",
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


class DetPagtoParc225Template(BaseTemplate):
    """Template for DETPAGTOPARC225 - Consultar Detalhes de Pagamento."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PERTMEI",
            id_servico="DETPAGTOPARC225",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - numeroParcelamento: int (parcelamento number)
                - anoMesParcela: int (year-month in format YYYYMM, e.g., 201907)

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
        # Validate format YYYYMM (e.g., 201907 = July 2019)
        if ano_mes < 190000 or ano_mes > 210012:
            raise ValidationError("Field 'anoMesParcela' must be in YYYYMM format (e.g., 201907)")

        return {
            "numeroParcelamento": numero,
            "anoMesParcela": ano_mes,
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("PERTMEI", "PEDIDOSPARC223", PedidosParc223Template)
TemplateRegistry.register("PERTMEI", "OBTERPARC224", ObterParc224Template)
TemplateRegistry.register("PERTMEI", "PARCELASPARAGERAR222", ParcelasParaGerar222Template)
TemplateRegistry.register("PERTMEI", "DETPAGTOPARC225", DetPagtoParc225Template)

