"""REGIME APURACAO system templates."""

# Import templates to register them
from integra_sdk.templates.regimeapuracao.consultar import (
    ConsultarAnosCalendarios102Template,
    ConsultarOpcaoRegime103Template,
    ConsultarResolucao104Template,
)
from integra_sdk.templates.regimeapuracao.declarar import EfetuarOpcaoRegime101Template

__all__ = [
    "EfetuarOpcaoRegime101Template",
    "ConsultarAnosCalendarios102Template",
    "ConsultarOpcaoRegime103Template",
    "ConsultarResolucao104Template",
]


