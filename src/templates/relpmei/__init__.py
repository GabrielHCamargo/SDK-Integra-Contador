"""RELPMEI system templates."""

# Import templates to register them
from integra_sdk.templates.relpmei.consultar import (
    PedidosParc233Template,
    ObterParc234Template,
    ParcelasParaGerar232Template,
    DetPagtoParc235Template,
)
from integra_sdk.templates.relpmei.emitir import Gerardas231Template

__all__ = [
    "PedidosParc233Template",
    "ObterParc234Template",
    "ParcelasParaGerar232Template",
    "DetPagtoParc235Template",
    "Gerardas231Template",
]


