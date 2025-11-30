"""Template registry for managing request templates."""

from typing import Type

from integra_sdk.templates.base import BaseTemplate


class TemplateRegistry:
    """Global registry for request templates."""

    _registry: dict[tuple[str, str], Type[BaseTemplate]] = {}

    @classmethod
    def register(
        cls,
        id_sistema: str,
        id_servico: str,
        template_class: Type[BaseTemplate],
    ):
        """Register a template class.

        Args:
            id_sistema: System ID
            id_servico: Service ID
            template_class: Template class to register
        """
        key = (id_sistema.upper(), id_servico.upper())
        cls._registry[key] = template_class

    @classmethod
    def get(cls, id_sistema: str, id_servico: str) -> Type[BaseTemplate] | None:
        """Get a template class by system and service ID.

        Args:
            id_sistema: System ID
            id_servico: Service ID

        Returns:
            Template class or None if not found
        """
        key = (id_sistema.upper(), id_servico.upper())
        return cls._registry.get(key)

    @classmethod
    def is_registered(cls, id_sistema: str, id_servico: str) -> bool:
        """Check if a template is registered.

        Args:
            id_sistema: System ID
            id_servico: Service ID

        Returns:
            True if template is registered
        """
        key = (id_sistema.upper(), id_servico.upper())
        return key in cls._registry

    @classmethod
    def clear(cls):
        """Clear all registered templates."""
        cls._registry.clear()

