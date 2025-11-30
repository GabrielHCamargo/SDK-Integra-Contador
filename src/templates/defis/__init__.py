"""DEFIS system templates."""

# Import templates to register them
from integra_sdk.templates.defis.declarar import TransDeclaracao141Template
from integra_sdk.templates.defis.consultar import (
    ConsDeclaracao142Template,
    ConsUltimaDecRec143Template,
    ConsDecRec144Template,
)

__all__ = [
    "TransDeclaracao141Template",
    "ConsDeclaracao142Template",
    "ConsUltimaDecRec143Template",
    "ConsDecRec144Template",
]

