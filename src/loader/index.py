"""Template index mapping (sistema, servico) to template classes."""

from typing import Type

from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


def get_template_class(id_sistema: str, id_servico: str) -> Type[BaseTemplate] | None:
    """Get template class for given system and service.

    Args:
        id_sistema: System ID
        id_servico: Service ID

    Returns:
        Template class or None if not found
    """
    return TemplateRegistry.get(id_sistema, id_servico)


def is_template_available(id_sistema: str, id_servico: str) -> bool:
    """Check if a template is available.

    Args:
        id_sistema: System ID
        id_servico: Service ID

    Returns:
        True if template is available
    """
    return TemplateRegistry.is_registered(id_sistema, id_servico)

