"""PARCMEI-ESP system templates."""

# Import templates to register them
from integra_sdk.templates.parcmeiesp.consultar import (
    PedidosParc213Template,
    ObterParc214Template,
    ParcelasParaGerar212Template,
    DetPagtoParc215Template,
)
from integra_sdk.templates.parcmeiesp.emitir import Gerardas211Template

__all__ = [
    "PedidosParc213Template",
    "ObterParc214Template",
    "ParcelasParaGerar212Template",
    "DetPagtoParc215Template",
    "Gerardas211Template",
]

