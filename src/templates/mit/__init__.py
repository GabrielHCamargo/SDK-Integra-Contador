"""MIT system templates."""

# Import templates to register them
from integra_sdk.templates.mit.declarar import Encapuracao314Template
from integra_sdk.templates.mit.apoiar import SituacaoEnc315Template
from integra_sdk.templates.mit.consultar import (
    ConsApuracao316Template,
    ListaApuracoes317Template,
)

__all__ = [
    "Encapuracao314Template",
    "SituacaoEnc315Template",
    "ConsApuracao316Template",
    "ListaApuracoes317Template",
]

