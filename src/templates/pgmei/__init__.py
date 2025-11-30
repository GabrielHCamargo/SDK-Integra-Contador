"""PGMEI system templates."""

# Import templates to register them
from integra_sdk.templates.pgmei.emitir import (
    GerardasPdf21Template,
    GerardasCodBarra22Template,
    AtuBeneficio23Template,
)
from integra_sdk.templates.pgmei.consultar import ConsDividaAtiva24Template

__all__ = [
    "GerardasPdf21Template",
    "GerardasCodBarra22Template",
    "AtuBeneficio23Template",
    "ConsDividaAtiva24Template",
]


