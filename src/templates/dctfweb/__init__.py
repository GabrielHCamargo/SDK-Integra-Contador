"""DCTFWEB system templates."""

# Import templates to register them
from integra_sdk.templates.dctfweb.consultar import (
    ConsultarRecibo32Template,
    ConsultarRelatorioCompleta33Template,
    ConsultarXmlDeclaracao38Template,
)
from integra_sdk.templates.dctfweb.emitir import (
    GerarGuia31Template,
    GerarGuiaAndamento313Template,
)
from integra_sdk.templates.dctfweb.transmitir import TransmitirDeclaracao310Template

__all__ = [
    "ConsultarRecibo32Template",
    "ConsultarRelatorioCompleta33Template",
    "ConsultarXmlDeclaracao38Template",
    "GerarGuia31Template",
    "GerarGuiaAndamento313Template",
    "TransmitirDeclaracao310Template",
]
