"""SICALC system templates."""

# Import templates to register them
from integra_sdk.templates.sicalc.emitir import (
    ConsolidarGerarDarf51Template,
    GerarDarfCodBarra53Template,
)
from integra_sdk.templates.sicalc.apoiar import ConsultaApoioReceitas52Template

__all__ = [
    "ConsolidarGerarDarf51Template",
    "ConsultaApoioReceitas52Template",
    "GerarDarfCodBarra53Template",
]


