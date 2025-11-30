"""Template loading utilities."""

from typing import Type

from integra_sdk.exceptions import RequestNotFoundError
from integra_sdk.loader.index import get_template_class
from integra_sdk.templates.base import BaseTemplate


def load_template(id_sistema: str, id_servico: str) -> BaseTemplate:
    """Load a template instance for the given system and service.

    Args:
        id_sistema: System ID
        id_servico: Service ID

    Returns:
        Template instance

    Raises:
        RequestNotFoundError: If template is not found
    """
    template_class = get_template_class(id_sistema, id_servico)

    if template_class is None:
        raise RequestNotFoundError(id_sistema, id_servico)

    return template_class()

