"""CAIXAPOSTAL - Monitorar response parsers."""

from typing import Any

from integra_sdk.responses.base import BaseResponseParser
from integra_sdk.responses.registry import ResponseParserRegistry


class InnoVamsg63ResponseParser(BaseResponseParser):
    """Parser for INNOVAMSG63 responses."""

    def __init__(self):
        """Initialize parser."""
        super().__init__(
            id_sistema="CAIXAPOSTAL",
            id_servico="INNOVAMSG63",
        )

    def _parse_dados(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Parse the dados field for INNOVAMSG63.

        Returns the data exactly as provided by the API, without transformations.
        Only performs basic JSON parsing if needed. All field names are preserved
        in their original format (camelCase, etc.).

        Args:
            dados: Parsed dados dictionary (from JSON string)

        Returns:
            Dados dictionary in the exact format provided by the API
        """
        # Return dados as-is, without any transformations
        # This preserves all field names in their original format (camelCase)
        return dados


# Register parser
ResponseParserRegistry.register(
    "CAIXAPOSTAL", "INNOVAMSG63", InnoVamsg63ResponseParser
)

