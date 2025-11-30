"""Response building utilities."""

from typing import Any
import json


class ResponseBuilder:
    """Builds structured responses from raw API responses.

    Returns data in the exact format provided by the API, without custom transformations.
    Only performs basic JSON parsing of the 'dados' field if it's a string.
    """

    @staticmethod
    def build(
        id_sistema: str,
        id_servico: str,
        raw_response: dict[str, Any],
    ) -> dict[str, Any]:
        """Build a response from raw API response.

        Returns the data exactly as provided by the API, with minimal processing:
        - Preserves all field names in their original format (camelCase, etc.)
        - Only parses the 'dados' field from JSON string to dict if needed
        - No field name transformations or custom parsing

        Args:
            id_sistema: System ID (kept for compatibility, not used)
            id_servico: Service ID (kept for compatibility, not used)
            raw_response: Raw response dictionary from API

        Returns:
            Response dictionary in the same format as the API
        """
        # Return response as-is, only parse 'dados' if it's a JSON string
        parsed = raw_response.copy()

        # Parse 'dados' field if it's a string (JSON)
        dados_value = parsed.get("dados")
        if isinstance(dados_value, str) and dados_value.strip():
            try:
                parsed["dados"] = json.loads(dados_value)
            except (json.JSONDecodeError, TypeError):
                # If parsing fails, keep as string
                parsed["dados"] = dados_value
        # If dados is already a dict/list or None, keep it as-is

        return parsed
