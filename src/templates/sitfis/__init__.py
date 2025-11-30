"""SITFIS system templates."""

# Import templates to register them
from integra_sdk.templates.sitfis.apoiar import SolicitarProtocolo91Template
from integra_sdk.templates.sitfis.emitir import RelatorioSitfis92Template

__all__ = [
    "SolicitarProtocolo91Template",
    "RelatorioSitfis92Template",
]


