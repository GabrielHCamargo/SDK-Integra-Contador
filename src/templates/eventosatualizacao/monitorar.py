"""EVENTOS ATUALIZACAO - Monitorar templates."""

from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class SoliEventosPf131Template(BaseTemplate):
    """Template for SOLICEVENTOSPF131 - Solicitar eventos de PF."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="EVENTOSATUALIZACAO",
            id_servico="SOLICEVENTOSPF131",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - evento: str (event code, e.g., "E0301")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["evento"]
        self._validate_required_fields(dados, required_fields)

        # Validate evento
        evento = dados["evento"]
        if not isinstance(evento, str):
            raise ValidationError("Field 'evento' must be a string")
        if not evento.strip():
            raise ValidationError("Field 'evento' cannot be empty")

        return {"evento": evento.strip()}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Monitorar"


class ObterEventosPf133Template(BaseTemplate):
    """Template for OBTEREVENTOSPF133 - Obter eventos de PF."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="EVENTOSATUALIZACAO",
            id_servico="OBTEREVENTOSPF133",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - protocolo: str (protocol ID from solicitation)
                - evento: str (event code, e.g., "E0301")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["protocolo", "evento"]
        self._validate_required_fields(dados, required_fields)

        # Validate protocolo
        protocolo = dados["protocolo"]
        if not isinstance(protocolo, str):
            raise ValidationError("Field 'protocolo' must be a string")
        if not protocolo.strip():
            raise ValidationError("Field 'protocolo' cannot be empty")

        # Validate evento
        evento = dados["evento"]
        if not isinstance(evento, str):
            raise ValidationError("Field 'evento' must be a string")
        if not evento.strip():
            raise ValidationError("Field 'evento' cannot be empty")

        return {
            "protocolo": protocolo.strip(),
            "evento": evento.strip(),
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Monitorar"


class SoliEventosPj132Template(BaseTemplate):
    """Template for SOLICEVENTOSPJ132 - Solicitar eventos de PJ."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="EVENTOSATUALIZACAO",
            id_servico="SOLICEVENTOSPJ132",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required field:
                - evento: str (event code, e.g., "E0301")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["evento"]
        self._validate_required_fields(dados, required_fields)

        # Validate evento
        evento = dados["evento"]
        if not isinstance(evento, str):
            raise ValidationError("Field 'evento' must be a string")
        if not evento.strip():
            raise ValidationError("Field 'evento' cannot be empty")

        return {"evento": evento.strip()}

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Monitorar"


class ObterEventosPj134Template(BaseTemplate):
    """Template for OBTEREVENTOSPJ134 - Obter eventos de PJ."""

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="EVENTOSATUALIZACAO",
            id_servico="OBTEREVENTOSPJ134",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - protocolo: str (protocol ID from solicitation)
                - evento: str (event code, e.g., "E0301")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = ["protocolo", "evento"]
        self._validate_required_fields(dados, required_fields)

        # Validate protocolo
        protocolo = dados["protocolo"]
        if not isinstance(protocolo, str):
            raise ValidationError("Field 'protocolo' must be a string")
        if not protocolo.strip():
            raise ValidationError("Field 'protocolo' cannot be empty")

        # Validate evento
        evento = dados["evento"]
        if not isinstance(evento, str):
            raise ValidationError("Field 'evento' must be a string")
        if not evento.strip():
            raise ValidationError("Field 'evento' cannot be empty")

        return {
            "protocolo": protocolo.strip(),
            "evento": evento.strip(),
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Monitorar"


# Register templates
TemplateRegistry.register("EVENTOSATUALIZACAO", "SOLICEVENTOSPF131", SoliEventosPf131Template)
TemplateRegistry.register("EVENTOSATUALIZACAO", "OBTEREVENTOSPF133", ObterEventosPf133Template)
TemplateRegistry.register("EVENTOSATUALIZACAO", "SOLICEVENTOSPJ132", SoliEventosPj132Template)
TemplateRegistry.register("EVENTOSATUALIZACAO", "OBTEREVENTOSPJ134", ObterEventosPj134Template)

