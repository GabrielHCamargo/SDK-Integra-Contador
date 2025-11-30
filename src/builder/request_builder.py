"""Request building utilities."""

from typing import Any

from integra_sdk.config import IntegraConfig
from integra_sdk.loader.template_loader import load_template
from integra_sdk.templates.base import BaseTemplate


class RequestBuilder:
    """Builds API requests from templates and data."""

    @staticmethod
    def build(
        config: IntegraConfig,
        id_sistema: str,
        id_servico: str,
        dados: dict[str, Any],
    ) -> tuple[BaseTemplate, dict[str, Any]]:
        """Build a request from template and data.

        Args:
            config: SDK configuration
            id_sistema: System ID
            id_servico: Service ID
            dados: Service-specific data

        Returns:
            Tuple of (template instance, request body)
        """
        # Load template
        template = load_template(id_sistema, id_servico)

        # Build request body
        request_body = template.build_request(config, dados)

        return template, request_body

