"""PGDAS-D system templates."""

# Import templates to register them
from integra_sdk.templates.pgdasd.consultar import (
    ConsDeclaracao13Template,
    ConsultimaDecRec14Template,
    ConsDecRec15Template,
    ConsExtrato16Template,
)
from integra_sdk.templates.pgdasd.emitir import (
    Gerardas12Template,
    GerardasAvulso19Template,
    GerardasCobranca17Template,
    GerardasProcesso18Template,
)
from integra_sdk.templates.pgdasd.declarar import TransDeclaracao11Template

__all__ = [
    "ConsDeclaracao13Template",
    "Gerardas12Template",
    "ConsultimaDecRec14Template",
    "ConsDecRec15Template",
    "ConsExtrato16Template",
    "TransDeclaracao11Template",
    "GerardasAvulso19Template",
    "GerardasCobranca17Template",
    "GerardasProcesso18Template",
]


