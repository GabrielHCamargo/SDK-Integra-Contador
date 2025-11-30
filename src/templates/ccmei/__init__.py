"""CCMEI system templates."""

# Import templates to register them
from integra_sdk.templates.ccmei.consultar import (
    CcmeiSitCadastral123Template,
    DadosCcmei122Template,
)
from integra_sdk.templates.ccmei.emitir import EmitirCcmei121Template

__all__ = [
    "CcmeiSitCadastral123Template",
    "DadosCcmei122Template",
    "EmitirCcmei121Template",
]

