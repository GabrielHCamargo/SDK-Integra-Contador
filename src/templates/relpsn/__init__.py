"""RELPSN system templates."""

# Import templates to register them
from integra_sdk.templates.relpsn.consultar import (
    PedidosParc193Template,
    ObterParc174Template,
    ParcelasParaGerar192Template,
    DetPagtoParc195Template,
)
from integra_sdk.templates.relpsn.emitir import Gerardas191Template

__all__ = [
    "PedidosParc193Template",
    "ObterParc174Template",
    "ParcelasParaGerar192Template",
    "DetPagtoParc195Template",
    "Gerardas191Template",
]


