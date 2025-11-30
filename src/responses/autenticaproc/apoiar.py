"""AUTENTICAPROCURADOR - Apoiar response parsers."""

from datetime import datetime
from typing import Any

from integra_sdk.responses.base import BaseResponseParser
from integra_sdk.responses.registry import ResponseParserRegistry


class EnvioXMLAssinado81ResponseParser(BaseResponseParser):
    """Parser for ENVIOXMLASSINADO81 responses."""

    def __init__(self):
        """Initialize parser."""
        super().__init__(
            id_sistema="AUTENTICAPROCURADOR",
            id_servico="ENVIOXMLASSINADO81",
        )

    def _parse_dados(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Parse the dados field for ENVIOXMLASSINADO81.

        Args:
            dados: Parsed dados dictionary

        Returns:
            Structured dados dictionary with:
                - autenticar_procurador_token: str
                - data_hora_expiracao: str (ISO format datetime)
                - data_hora_expiracao_datetime: datetime | None (parsed datetime, if valid)
        """
        parsed = {
            "autenticar_procurador_token": dados.get("autenticar_procurador_token"),
            "data_hora_expiracao": dados.get("data_hora_expiracao"),
        }

        # Try to parse the expiration datetime (optional)
        data_hora_expiracao_str = dados.get("data_hora_expiracao")
        if data_hora_expiracao_str:
            try:
                # Try to parse ISO format datetime
                # Format example: "2022-08-12T16:38:02.4163946-03:00"
                # Python's fromisoformat might need some cleanup for extended formats
                dt_str = data_hora_expiracao_str
                # Remove timezone if present for simpler parsing
                if dt_str.endswith(("Z", "+00:00", "-00:00")):
                    dt_str = dt_str.rstrip("Z+-00:00")
                parsed["data_hora_expiracao_datetime"] = datetime.fromisoformat(dt_str)
            except (ValueError, AttributeError):
                # If parsing fails, leave as None - the string is still available
                parsed["data_hora_expiracao_datetime"] = None
        else:
            parsed["data_hora_expiracao_datetime"] = None

        return parsed


# Register parser
ResponseParserRegistry.register(
    "AUTENTICAPROCURADOR", "ENVIOXMLASSINADO81", EnvioXMLAssinado81ResponseParser
)

