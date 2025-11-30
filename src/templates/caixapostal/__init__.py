"""CAIXAPOSTAL system templates."""

# Import templates to register them
from integra_sdk.templates.caixapostal.consultar import (
    MsgContribuinte61Template,
    MsgDetalhamento62Template,
)
from integra_sdk.templates.caixapostal.monitorar import InnoVamsg63Template

__all__ = [
    "MsgContribuinte61Template",
    "MsgDetalhamento62Template",
    "InnoVamsg63Template",
]
