"""CAIXAPOSTAL - Consultar response parsers."""

from typing import Any

from integra_sdk.responses.base import BaseResponseParser
from integra_sdk.responses.registry import ResponseParserRegistry


class MsgDetalhamento62ResponseParser(BaseResponseParser):
    """Parser for MSGDETALHAMENTO62 responses."""

    def __init__(self):
        """Initialize parser."""
        super().__init__(
            id_sistema="CAIXAPOSTAL",
            id_servico="MSGDETALHAMENTO62",
        )

    def _parse_dados(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Parse the dados field for MSGDETALHAMENTO62.

        Args:
            dados: Parsed dados dictionary

        Returns:
            Structured dados dictionary
        """
        parsed = {
            "codigo": dados.get("codigo"),
            "sucesso": dados.get("codigo") == "00",
        }

        # Parse conteudo (array of messages)
        conteudo = dados.get("conteudo", [])
        if conteudo:
            parsed["mensagens"] = [
                self._parse_mensagem(msg) for msg in conteudo
            ]
        else:
            parsed["mensagens"] = []

        return parsed

    def _parse_mensagem(self, msg: dict[str, Any]) -> dict[str, Any]:
        """Parse a single message from conteudo.

        Args:
            msg: Message dictionary

        Returns:
            Structured message dictionary
        """
        return {
            "codigo_sistema_remetente": msg.get("codigoSistemaRemetente"),
            "codigo_modelo": msg.get("codigoModelo"),
            "assunto": msg.get("assuntoModelo"),
            "origem": msg.get("origemModelo"),
            "data_envio": msg.get("dataEnvio"),
            "data_leitura": msg.get("dataLeitura"),
            "hora_leitura": msg.get("horaLeitura"),
            "data_expiracao": msg.get("dataExpiracao"),
            "numero_controle": msg.get("numeroControle"),
            "data_ciencia": msg.get("dataCiencia"),
            "enquadramento": msg.get("enquadramento"),
            "data_acesso_externo": msg.get("dataAcessoExterno"),
            "hora_acesso_externo": msg.get("horaAcessoExterno"),
            "tipo_autenticacao": msg.get("tipoAutenticacaoUsuario"),
            "codigo_acesso": msg.get("codigoAcesso"),
            "numero_serie_certificado": msg.get("numeroSerieCertificadoDigital"),
            "emissor_certificado": msg.get("emissorCertificadoDigital"),
            "tipo_usuario": msg.get("tipoUsuario"),
            "ni_usuario": msg.get("niUsuario"),
            "papel_usuario": msg.get("papelUsuario"),
            "codigo_aplicacao": msg.get("codigoAplicacao"),
            "tipo_origem": msg.get("tipoOrigem"),
            "descricao_origem": msg.get("descricaoOrigem"),
            "corpo": msg.get("corpoModelo"),
            "variaveis": msg.get("variaveis", []),
            "valor_parametro_assunto": msg.get("valorParametroAssunto"),
        }


# Register parser
ResponseParserRegistry.register(
    "CAIXAPOSTAL", "MSGDETALHAMENTO62", MsgDetalhamento62ResponseParser
)




