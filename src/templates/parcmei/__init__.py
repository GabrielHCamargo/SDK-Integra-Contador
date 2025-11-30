"""PARCMEI system templates."""

# Import templates to register them
from integra_sdk.templates.parcmei.consultar import (
    PedidosParc203Template,
    ObterParc204Template,
    ParcelasParaGerar202Template,
    DetPagtoParc205Template,
)
from integra_sdk.templates.parcmei.emitir import Gerardas201Template

__all__ = [
    "PedidosParc203Template",
    "ObterParc204Template",
    "ParcelasParaGerar202Template",
    "DetPagtoParc205Template",
    "Gerardas201Template",
]

