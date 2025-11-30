"""PERTMEI system templates."""

# Import templates to register them
from integra_sdk.templates.pertmei.consultar import (
    PedidosParc223Template,
    ObterParc224Template,
    ParcelasParaGerar222Template,
    DetPagtoParc225Template,
)
from integra_sdk.templates.pertmei.emitir import Gerardas221Template

__all__ = [
    "PedidosParc223Template",
    "ObterParc224Template",
    "ParcelasParaGerar222Template",
    "DetPagtoParc225Template",
    "Gerardas221Template",
]

