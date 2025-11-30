"""Response parser registry."""

from typing import Any

from integra_sdk.responses.base import BaseResponseParser


class ResponseParserRegistry:
    """Registry for response parsers."""

    _parsers: dict[tuple[str, str], type[BaseResponseParser]] = {}

    @classmethod
    def register(
        cls,
        id_sistema: str,
        id_servico: str,
        parser_class: type[BaseResponseParser],
    ) -> None:
        """Register a response parser.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            parser_class: Parser class
        """
        key = (id_sistema.upper(), id_servico.upper())
        cls._parsers[key] = parser_class

    @classmethod
    def get_parser(
        cls, id_sistema: str, id_servico: str
    ) -> BaseResponseParser | None:
        """Get a response parser for the given system and service.

        Args:
            id_sistema: System ID
            id_servico: Service ID

        Returns:
            Parser instance or None if not found
        """
        key = (id_sistema.upper(), id_servico.upper())
        parser_class = cls._parsers.get(key)
        if parser_class:
            # Try to instantiate without parameters first (for specific parsers)
            # If that fails, try with parameters (for generic parsers)
            try:
                return parser_class()
            except TypeError:
                return parser_class(id_sistema, id_servico)
        return None

    @classmethod
    def has_parser(cls, id_sistema: str, id_servico: str) -> bool:
        """Check if a parser exists for the given system and service.

        Args:
            id_sistema: System ID
            id_servico: Service ID

        Returns:
            True if parser exists, False otherwise
        """
        key = (id_sistema.upper(), id_servico.upper())
        return key in cls._parsers

