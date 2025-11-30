"""PARCSN system templates."""

# Import templates to register them
from integra_sdk.templates.parcsn.consultar import (
    PedidosParc163Template,
    ObterParc164Template,
    ParcelasParaGerar162Template,
    DetPagtoParc165Template,
)
from integra_sdk.templates.parcsn.emitir import Gerardas161Template

__all__ = [
    "PedidosParc163Template",
    "ObterParc164Template",
    "ParcelasParaGerar162Template",
    "DetPagtoParc165Template",
    "Gerardas161Template",
]

