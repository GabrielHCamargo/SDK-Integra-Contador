"""Unit tests for AUTENTICAPROCURADOR template."""

import base64
from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.responses.autenticaproc.apoiar import EnvioXMLAssinado81ResponseParser
from integra_sdk.templates.autenticaproc.apoiar import EnvioXMLAssinado81Template
from integra_sdk.templates.registry import TemplateRegistry


class TestEnvioXMLAssinado81Template:
    """Tests for EnvioXMLAssinado81Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return EnvioXMLAssinado81Template()

    @pytest.fixture
    def valid_xml_base64(self):
        """Fixture with valid base64 encoded XML."""
        xml_content = """<termoDeAutorizacao>
            <dados>
                <sistema id="API Integra Contador" />
                <termo texto="Autorizo a empresa CONTRATANTE..." />
            </dados>
        </termoDeAutorizacao>"""
        return base64.b64encode(xml_content.encode("utf-8")).decode("utf-8")

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "AUTENTICAPROCURADOR"
        assert template.id_servico == "ENVIOXMLASSINADO81"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Apoiar"

    def test_validate_success(self, template, valid_xml_base64):
        """Test successful validation with valid data."""
        dados = {"xml": valid_xml_base64}
        result = template.validate(dados)
        
        assert result == {"xml": valid_xml_base64}
        assert isinstance(result["xml"], str)

    def test_validate_missing_xml(self, template):
        """Test validation fails when xml field is missing."""
        dados = {}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "missing" in str(exc_info.value).lower() or "required" in str(exc_info.value).lower()

    def test_validate_empty_xml(self, template):
        """Test validation fails when xml is empty."""
        dados = {"xml": ""}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "empty" in str(exc_info.value).lower() or "cannot" in str(exc_info.value).lower()

    def test_validate_whitespace_only_xml(self, template):
        """Test validation fails when xml is only whitespace."""
        dados = {"xml": "   \n\t   "}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "empty" in str(exc_info.value).lower() or "cannot" in str(exc_info.value).lower()

    def test_validate_invalid_base64(self, template):
        """Test validation fails when xml is not valid base64."""
        dados = {"xml": "not-valid-base64-!!!123"}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "base64" in str(exc_info.value).lower()

    def test_validate_invalid_type(self, template):
        """Test validation fails when xml is not a string."""
        dados = {"xml": 12345}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "string" in str(exc_info.value).lower()

    def test_validate_strips_whitespace(self, template, valid_xml_base64):
        """Test that validation strips whitespace from xml."""
        dados = {"xml": f"  {valid_xml_base64}  \n"}
        result = template.validate(dados)
        
        assert result["xml"] == valid_xml_base64

    def test_build_request(self, template, valid_xml_base64):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "11111111111111", "tipo": 2}
        
        dados = {"xml": valid_xml_base64}
        request = template.build_request(config, dados)
        
        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request
        
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "AUTENTICAPROCURADOR"
        assert pedido_dados["idServico"] == "ENVIOXMLASSINADO81"
        assert pedido_dados["versaoSistema"] == "1.0"
        
        # Verify dados is JSON string containing the xml
        import json
        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["xml"] == valid_xml_base64

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("AUTENTICAPROCURADOR", "ENVIOXMLASSINADO81")
        assert template_class is not None
        assert template_class == EnvioXMLAssinado81Template


class TestEnvioXMLAssinado81ResponseParser:
    """Tests for EnvioXMLAssinado81ResponseParser."""

    @pytest.fixture
    def parser(self):
        """Fixture creating a parser instance."""
        return EnvioXMLAssinado81ResponseParser()

    def test_init(self, parser):
        """Test parser initialization."""
        assert parser.id_sistema == "AUTENTICAPROCURADOR"
        assert parser.id_servico == "ENVIOXMLASSINADO81"

    def test_parse_dados_success(self, parser):
        """Test parsing valid dados."""
        dados = {
            "autenticar_procurador_token": "b06feea3-1ca8-49f4-bdb4-211ab006cb92",
            "data_hora_expiracao": "2022-08-12T16:38:02.4163946-03:00",
        }
        
        result = parser._parse_dados(dados)
        
        assert result["autenticar_procurador_token"] == "b06feea3-1ca8-49f4-bdb4-211ab006cb92"
        assert result["data_hora_expiracao"] == "2022-08-12T16:38:02.4163946-03:00"
        # datetime parsing may fail or succeed depending on format complexity
        assert "data_hora_expiracao_datetime" in result

    def test_parse_dados_missing_fields(self, parser):
        """Test parsing dados with missing fields."""
        dados = {}
        
        result = parser._parse_dados(dados)
        
        assert result["autenticar_procurador_token"] is None
        assert result["data_hora_expiracao"] is None
        assert result["data_hora_expiracao_datetime"] is None

    def test_parse_full_response(self, parser):
        """Test parsing full response."""
        raw_response = {
            "status": 200,
            "mensagens": [
                {"codigo": "[Sucesso-AUTENTICAPROCURADOR]", "texto": "Requisição efetuada com sucesso."}
            ],
            "contratante": {"numero": "99999999999999", "tipo": 2},
            "autorPedidoDados": {"numero": "00000000000000", "tipo": 2},
            "contribuinte": {"numero": "11111111111111", "tipo": 2},
            "pedidoDados": {
                "idSistema": "AUTENTICAPROCURADOR",
                "idServico": "ENVIOXMLASSINADO81",
                "versaoSistema": "1.0",
            },
            "dados": '{"autenticar_procurador_token": "b06feea3-1ca8-49f4-bdb4-211ab006cb92", "data_hora_expiracao": "2022-08-12T16:38:02.4163946-03:00"}',
        }
        
        result = parser.parse(raw_response)
        
        assert result["status"] == 200
        assert len(result["mensagens"]) == 1
        assert result["mensagens"][0]["codigo"] == "[Sucesso-AUTENTICAPROCURADOR]"
        assert "dados" in result
        assert result["dados"]["autenticar_procurador_token"] == "b06feea3-1ca8-49f4-bdb4-211ab006cb92"
        assert "data_hora_expiracao" in result["dados"]

