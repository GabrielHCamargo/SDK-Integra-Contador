"""PERTSN system templates."""

# Import templates to register them
from integra_sdk.templates.pertsn.consultar import (
    PedidosParc183Template,
    ObterParc184Template,
    ParcelasParaGerar182Template,
    DetPagtoParc185Template,
)
from integra_sdk.templates.pertsn.emitir import Gerardas181Template

__all__ = [
    "PedidosParc183Template",
    "ObterParc184Template",
    "ParcelasParaGerar182Template",
    "DetPagtoParc185Template",
    "Gerardas181Template",
]

