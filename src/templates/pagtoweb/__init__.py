"""PAGTOWEB system templates."""

# Import templates to register them
from integra_sdk.templates.pagtoweb.consultar import (
    Pagamentos71Template,
    ContaConsDocArrPg73Template,
)
from integra_sdk.templates.pagtoweb.emitir import Comparrecadacao72Template

__all__ = [
    "Pagamentos71Template",
    "ContaConsDocArrPg73Template",
    "Comparrecadacao72Template",
]

