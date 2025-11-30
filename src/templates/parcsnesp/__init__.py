"""PARCSN-ESP system templates."""

# Import templates to register them
from integra_sdk.templates.parcsnesp.consultar import (
    PedidosParc173Template,
    ObterParc174Template,
    ParcelasParaGerar172Template,
    DetPagtoParc175Template,
)
from integra_sdk.templates.parcsnesp.emitir import Gerardas171Template

__all__ = [
    "PedidosParc173Template",
    "ObterParc174Template",
    "ParcelasParaGerar172Template",
    "DetPagtoParc175Template",
    "Gerardas171Template",
]

