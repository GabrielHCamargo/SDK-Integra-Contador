"""CCMEI - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class CcmeiSitCadastral123Template(BaseTemplate):
    """Template for CCMEISITCADASTRAL123 - Consulta a situação cadastral dos CNPJ MEI vinculados ao CPF."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="CCMEI",
            id_servico="CCMEISITCADASTRAL123",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary (should be empty for this service)

        Returns:
            Validated data (empty dict since this service requires no input)

        Raises:
            ValidationError: If validation fails

        Note:
            This service does not require any input data. The dados field
            should be an empty dictionary or can be omitted entirely.
            The CPF is determined from the contribuinte field in the request context.
        """
        # This service accepts empty dados or no dados at all
        # If dados is provided, it should be empty or only contain empty strings
        if dados:
            # If dados is provided, verify it's truly empty or only whitespace
            non_empty = {k: v for k, v in dados.items() if v and str(v).strip()}
            if non_empty:
                raise ValidationError(
                    f"Service CCMEISITCADASTRAL123 does not accept input data. "
                    f"Found unexpected fields: {list(non_empty.keys())}"
                )
        
        # Return empty dict (will be serialized as empty JSON string)
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados dictionary to JSON string.
        
        For this service, empty dict should serialize to empty string,
        not to "{}".

        Args:
            dados: Data dictionary (should be empty for this service)

        Returns:
            Empty string if dados is empty, otherwise JSON string
        """
        # For CCMEISITCADASTRAL123, empty dados should be serialized as empty string
        if not dados or (isinstance(dados, dict) and len(dados) == 0):
            return ""
        
        # If somehow dados is not empty, serialize normally
        import json
        return json.dumps(dados, ensure_ascii=False)


class DadosCcmei122Template(BaseTemplate):
    """Template for DADOSCCMEI122 - Consulta os dados do Certificado de Condição MEI."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="CCMEI",
            id_servico="DADOSCCMEI122",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary (should be empty for this service)

        Returns:
            Validated data (empty dict since this service requires no input)

        Raises:
            ValidationError: If validation fails

        Note:
            This service does not require any input data. The dados field
            should be an empty dictionary or can be omitted entirely.
            The CNPJ is determined from the contribuinte field in the request context.
        """
        # This service accepts empty dados or no dados at all
        # If dados is provided, it should be empty or only contain empty strings
        if dados:
            # If dados is provided, verify it's truly empty or only whitespace
            non_empty = {k: v for k, v in dados.items() if v and str(v).strip()}
            if non_empty:
                raise ValidationError(
                    f"Service DADOSCCMEI122 does not accept input data. "
                    f"Found unexpected fields: {list(non_empty.keys())}"
                )
        
        # Return empty dict (will be serialized as empty JSON string)
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"

    def _serialize_dados(self, dados: dict[str, Any]) -> str:
        """Serialize dados dictionary to JSON string.
        
        For this service, empty dict should serialize to empty string,
        not to "{}".

        Args:
            dados: Data dictionary (should be empty for this service)

        Returns:
            Empty string if dados is empty, otherwise JSON string
        """
        # For DADOSCCMEI122, empty dados should be serialized as empty string
        if not dados or (isinstance(dados, dict) and len(dados) == 0):
            return ""
        
        # If somehow dados is not empty, serialize normally
        import json
        return json.dumps(dados, ensure_ascii=False)


# Register templates
TemplateRegistry.register("CCMEI", "CCMEISITCADASTRAL123", CcmeiSitCadastral123Template)
TemplateRegistry.register("CCMEI", "DADOSCCMEI122", DadosCcmei122Template)

