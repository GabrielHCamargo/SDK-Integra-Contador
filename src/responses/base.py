"""Base response parser class."""

from abc import ABC, abstractmethod
from typing import Any

import json


class BaseResponseParser(ABC):
    """Base class for all response parsers."""

    def __init__(self, id_sistema: str, id_servico: str):
        """Initialize response parser.

        Args:
            id_sistema: System ID
            id_servico: Service ID
        """
        self.id_sistema = id_sistema
        self.id_servico = id_servico

    def parse(self, raw_response: dict[str, Any]) -> dict[str, Any]:
        """Parse the raw API response into a structured format.

        Args:
            raw_response: Raw response dictionary from API

        Returns:
            Parsed and structured response dictionary
        """
        # Extract common fields
        parsed = {
            "status": raw_response.get("status"),
            "mensagens": raw_response.get("mensagens", []),
            "metadata": {
                "contratante": raw_response.get("contratante"),
                "autorPedidoDados": raw_response.get("autorPedidoDados"),
                "contribuinte": raw_response.get("contribuinte"),
                "pedidoDados": raw_response.get("pedidoDados"),
            },
        }

        # Parse the dados field (JSON string)
        dados_str = raw_response.get("dados", "")
        if dados_str:
            try:
                dados_parsed = json.loads(dados_str)
                parsed["dados"] = self._parse_dados(dados_parsed)
            except (json.JSONDecodeError, TypeError) as e:
                parsed["dados"] = {"raw": dados_str, "parse_error": str(e)}
        else:
            parsed["dados"] = None

        return parsed

    @abstractmethod
    def _parse_dados(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Parse the dados field content.

        Args:
            dados: Parsed dados dictionary (from JSON string)

        Returns:
            Structured dados dictionary
        """
        pass

    def _extract_mensagens(self, raw_response: dict[str, Any]) -> list[dict[str, str]]:
        """Extract and format messages from response.

        Args:
            raw_response: Raw response dictionary

        Returns:
            List of message dictionaries
        """
        mensagens = raw_response.get("mensagens", [])
        return [
            {
                "codigo": msg.get("codigo", ""),
                "texto": msg.get("texto", ""),
            }
            for msg in mensagens
        ]




