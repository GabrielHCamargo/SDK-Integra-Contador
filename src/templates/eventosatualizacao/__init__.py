"""EVENTOS ATUALIZACAO system templates."""

# Import templates to register them
from integra_sdk.templates.eventosatualizacao.monitorar import (
    SoliEventosPf131Template,
    ObterEventosPf133Template,
    SoliEventosPj132Template,
    ObterEventosPj134Template,
)

__all__ = [
    "SoliEventosPf131Template",
    "ObterEventosPf133Template",
    "SoliEventosPj132Template",
    "ObterEventosPj134Template",
]

