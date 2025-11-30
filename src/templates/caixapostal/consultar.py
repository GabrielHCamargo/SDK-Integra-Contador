"""CAIXAPOSTAL - Consultar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class MsgDetalhamento62Template(BaseTemplate):
    """Template for MSGDETALHAMENTO62 - Obter Detalhes de uma Mensagem Específica."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="CAIXAPOSTAL",
            id_servico="MSGDETALHAMENTO62",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with 'isn' field

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        self._validate_required_fields(dados, ["isn"])

        isn = dados["isn"]
        if not isinstance(isn, str):
            raise ValidationError("Field 'isn' must be a string")

        if not isn.strip():
            raise ValidationError("Field 'isn' cannot be empty")

        return {"isn": isn.strip()}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class MsgContribuinte61Template(BaseTemplate):
    """Template for MSGCONTRIBUINTE61 - Obter Lista de Mensagens por Contribuintes."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="CAIXAPOSTAL",
            id_servico="MSGCONTRIBUINTE61",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with optional pagination fields:
                - statusLeitura: str (optional, default: "0")
                - indicadorPagina: str (optional, default: "0")
                - ponteiroPagina: str (optional, default: "00000000000000")

        Returns:
            Validated data dictionary

        Raises:
            ValidationError: If validation fails

        Note:
            All fields are optional. If not provided, defaults will be used:
            - statusLeitura: "0" (all messages)
            - indicadorPagina: "0" (first page)
            - ponteiroPagina: "00000000000000" (start from beginning)
        """
        validated: dict[str, Any] = {}

        # Validate statusLeitura (optional)
        if "statusLeitura" in dados:
            status_leitura = dados["statusLeitura"]
            if not isinstance(status_leitura, str):
                raise ValidationError("Field 'statusLeitura' must be a string")
            validated["statusLeitura"] = status_leitura.strip() or "0"
        else:
            validated["statusLeitura"] = "0"

        # Validate indicadorPagina (optional)
        if "indicadorPagina" in dados:
            indicador_pagina = dados["indicadorPagina"]
            if not isinstance(indicador_pagina, str):
                raise ValidationError("Field 'indicadorPagina' must be a string")
            validated["indicadorPagina"] = indicador_pagina.strip() or "0"
        else:
            validated["indicadorPagina"] = "0"

        # Validate ponteiroPagina (optional)
        if "ponteiroPagina" in dados:
            ponteiro_pagina = dados["ponteiroPagina"]
            if not isinstance(ponteiro_pagina, str):
                raise ValidationError("Field 'ponteiroPagina' must be a string")
            validated["ponteiroPagina"] = ponteiro_pagina.strip() or "00000000000000"
        else:
            validated["ponteiroPagina"] = "00000000000000"

        return validated

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("CAIXAPOSTAL", "MSGDETALHAMENTO62", MsgDetalhamento62Template)
TemplateRegistry.register("CAIXAPOSTAL", "MSGCONTRIBUINTE61", MsgContribuinte61Template)
