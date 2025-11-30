"""Unit tests for CAIXAPOSTAL templates and parsers."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.responses.caixapostal.consultar import MsgDetalhamento62ResponseParser
from integra_sdk.responses.caixapostal.monitorar import InnoVamsg63ResponseParser
from integra_sdk.templates.caixapostal.consultar import (
    MsgContribuinte61Template,
    MsgDetalhamento62Template,
)
from integra_sdk.templates.caixapostal.monitorar import InnoVamsg63Template
from integra_sdk.templates.registry import TemplateRegistry


class TestMsgDetalhamento62Template:
    """Tests for MsgDetalhamento62Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return MsgDetalhamento62Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "CAIXAPOSTAL"
        assert template.id_servico == "MSGDETALHAMENTO62"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid data."""
        dados = {"isn": "0000082838"}
        result = template.validate(dados)
        
        assert result == {"isn": "0000082838"}
        assert isinstance(result["isn"], str)

    def test_validate_missing_isn(self, template):
        """Test validation fails when isn field is missing."""
        dados = {}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "missing" in str(exc_info.value).lower() or "required" in str(exc_info.value).lower()

    def test_validate_empty_isn(self, template):
        """Test validation fails when isn is empty."""
        dados = {"isn": ""}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "empty" in str(exc_info.value).lower() or "cannot" in str(exc_info.value).lower()

    def test_validate_whitespace_only_isn(self, template):
        """Test validation fails when isn is only whitespace."""
        dados = {"isn": "   \n\t   "}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "empty" in str(exc_info.value).lower() or "cannot" in str(exc_info.value).lower()

    def test_validate_invalid_type(self, template):
        """Test validation fails when isn is not a string."""
        dados = {"isn": 12345}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "string" in str(exc_info.value).lower()

    def test_validate_strips_whitespace(self, template):
        """Test that validation strips whitespace from isn."""
        dados = {"isn": "  0000082838  \n"}
        result = template.validate(dados)
        
        assert result["isn"] == "0000082838"

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        
        dados = {"isn": "0000082838"}
        request = template.build_request(config, dados)
        
        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request
        
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "CAIXAPOSTAL"
        assert pedido_dados["idServico"] == "MSGDETALHAMENTO62"
        assert pedido_dados["versaoSistema"] == "1.0"
        
        # Verify dados is JSON string containing the isn
        import json
        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["isn"] == "0000082838"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("CAIXAPOSTAL", "MSGDETALHAMENTO62")
        assert template_class is not None
        assert template_class == MsgDetalhamento62Template


class TestMsgContribuinte61Template:
    """Tests for MsgContribuinte61Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return MsgContribuinte61Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "CAIXAPOSTAL"
        assert template.id_servico == "MSGCONTRIBUINTE61"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success_all_fields(self, template):
        """Test successful validation with all fields provided."""
        dados = {
            "statusLeitura": "0",
            "indicadorPagina": "1",
            "ponteiroPagina": "20220802160251",
        }
        result = template.validate(dados)
        
        assert result["statusLeitura"] == "0"
        assert result["indicadorPagina"] == "1"
        assert result["ponteiroPagina"] == "20220802160251"

    def test_validate_success_no_fields(self, template):
        """Test successful validation with no fields (uses defaults)."""
        dados = {}
        result = template.validate(dados)
        
        assert result["statusLeitura"] == "0"
        assert result["indicadorPagina"] == "0"
        assert result["ponteiroPagina"] == "00000000000000"

    def test_validate_success_partial_fields(self, template):
        """Test successful validation with partial fields."""
        dados = {"statusLeitura": "1"}
        result = template.validate(dados)
        
        assert result["statusLeitura"] == "1"
        assert result["indicadorPagina"] == "0"  # Default
        assert result["ponteiroPagina"] == "00000000000000"  # Default

    def test_validate_empty_string_fields(self, template):
        """Test that empty string fields use defaults."""
        dados = {
            "statusLeitura": "",
            "indicadorPagina": "",
            "ponteiroPagina": "",
        }
        result = template.validate(dados)
        
        assert result["statusLeitura"] == "0"
        assert result["indicadorPagina"] == "0"
        assert result["ponteiroPagina"] == "00000000000000"

    def test_validate_whitespace_fields(self, template):
        """Test that whitespace-only fields are trimmed and use defaults if empty."""
        dados = {
            "statusLeitura": "   ",
            "indicadorPagina": "  ",
            "ponteiroPagina": "    ",
        }
        result = template.validate(dados)
        
        assert result["statusLeitura"] == "0"
        assert result["indicadorPagina"] == "0"
        assert result["ponteiroPagina"] == "00000000000000"

    def test_validate_invalid_type_status_leitura(self, template):
        """Test validation fails when statusLeitura is not a string."""
        dados = {"statusLeitura": 0}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        error_msg = str(exc_info.value).lower()
        assert "statusleitura" in error_msg or "status" in error_msg

    def test_validate_invalid_type_indicador_pagina(self, template):
        """Test validation fails when indicadorPagina is not a string."""
        dados = {"indicadorPagina": 0}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        error_msg = str(exc_info.value).lower()
        assert "indicadorpagina" in error_msg or "indicador" in error_msg

    def test_validate_invalid_type_ponteiro_pagina(self, template):
        """Test validation fails when ponteiroPagina is not a string."""
        dados = {"ponteiroPagina": 0}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        error_msg = str(exc_info.value).lower()
        assert "ponteiropagina" in error_msg or "ponteiro" in error_msg

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        
        dados = {
            "statusLeitura": "0",
            "indicadorPagina": "0",
            "ponteiroPagina": "00000000000000",
        }
        request = template.build_request(config, dados)
        
        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request
        
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "CAIXAPOSTAL"
        assert pedido_dados["idServico"] == "MSGCONTRIBUINTE61"
        assert pedido_dados["versaoSistema"] == "1.0"
        
        # Verify dados is JSON string containing the fields
        import json
        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["statusLeitura"] == "0"
        assert dados_parsed["indicadorPagina"] == "0"
        assert dados_parsed["ponteiroPagina"] == "00000000000000"

    def test_build_request_defaults(self, template):
        """Test building request with default values when no fields provided."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        
        dados = {}
        request = template.build_request(config, dados)
        
        import json
        dados_parsed = json.loads(request["pedidoDados"]["dados"])
        assert dados_parsed["statusLeitura"] == "0"
        assert dados_parsed["indicadorPagina"] == "0"
        assert dados_parsed["ponteiroPagina"] == "00000000000000"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("CAIXAPOSTAL", "MSGCONTRIBUINTE61")
        assert template_class is not None
        assert template_class == MsgContribuinte61Template


class TestMsgDetalhamento62ResponseParser:
    """Tests for MsgDetalhamento62ResponseParser."""

    @pytest.fixture
    def parser(self):
        """Fixture creating a parser instance."""
        return MsgDetalhamento62ResponseParser()

    def test_init(self, parser):
        """Test parser initialization."""
        assert parser.id_sistema == "CAIXAPOSTAL"
        assert parser.id_servico == "MSGDETALHAMENTO62"

    def test_parse_dados_success_with_messages(self, parser):
        """Test parsing valid dados with messages."""
        dados = {
            "codigo": "00",
            "conteudo": [
                {
                    "codigoSistemaRemetente": "00014",
                    "codigoModelo": "00009",
                    "assuntoModelo": "Test Subject",
                    "origemModelo": "1",
                    "dataEnvio": "20220620",
                    "dataLeitura": "20220623",
                    "horaLeitura": "170051",
                    "dataExpiracao": "20230621",
                    "numeroControle": "12345",
                    "dataCiencia": "20220624",
                    "enquadramento": "0",
                    "dataAcessoExterno": "20220625",
                    "horaAcessoExterno": "100000",
                    "tipoAutenticacaoUsuario": "1",
                    "codigoAcesso": "ABC123",
                    "numeroSerieCertificadoDigital": "SERIE001",
                    "emissorCertificadoDigital": "EMISSOR",
                    "tipoUsuario": "1",
                    "niUsuario": "12345678901234",
                    "papelUsuario": "1",
                    "codigoAplicacao": "00001",
                    "tipoOrigem": "1",
                    "descricaoOrigem": "ORIGEM TESTE",
                    "corpoModelo": "<p>Test body</p>",
                    "variaveis": ["var1", "var2"],
                    "valorParametroAssunto": "VALOR123",
                }
            ],
        }
        
        result = parser._parse_dados(dados)
        
        assert result["codigo"] == "00"
        assert result["sucesso"] is True
        assert len(result["mensagens"]) == 1
        
        msg = result["mensagens"][0]
        assert msg["codigo_sistema_remetente"] == "00014"
        assert msg["codigo_modelo"] == "00009"
        assert msg["assunto"] == "Test Subject"
        assert msg["origem"] == "1"
        assert msg["data_envio"] == "20220620"
        assert msg["data_leitura"] == "20220623"
        assert msg["hora_leitura"] == "170051"
        assert msg["data_expiracao"] == "20230621"
        assert msg["numero_controle"] == "12345"
        assert msg["data_ciencia"] == "20220624"
        assert msg["enquadramento"] == "0"
        assert msg["data_acesso_externo"] == "20220625"
        assert msg["hora_acesso_externo"] == "100000"
        assert msg["tipo_autenticacao"] == "1"
        assert msg["codigo_acesso"] == "ABC123"
        assert msg["numero_serie_certificado"] == "SERIE001"
        assert msg["emissor_certificado"] == "EMISSOR"
        assert msg["tipo_usuario"] == "1"
        assert msg["ni_usuario"] == "12345678901234"
        assert msg["papel_usuario"] == "1"
        assert msg["codigo_aplicacao"] == "00001"
        assert msg["tipo_origem"] == "1"
        assert msg["descricao_origem"] == "ORIGEM TESTE"
        assert msg["corpo"] == "<p>Test body</p>"
        assert msg["variaveis"] == ["var1", "var2"]
        assert msg["valor_parametro_assunto"] == "VALOR123"

    def test_parse_dados_success_no_messages(self, parser):
        """Test parsing dados with no messages."""
        dados = {
            "codigo": "00",
            "conteudo": [],
        }
        
        result = parser._parse_dados(dados)
        
        assert result["codigo"] == "00"
        assert result["sucesso"] is True
        assert result["mensagens"] == []

    def test_parse_dados_error_code(self, parser):
        """Test parsing dados with error code."""
        dados = {
            "codigo": "99",
            "conteudo": [],
        }
        
        result = parser._parse_dados(dados)
        
        assert result["codigo"] == "99"
        assert result["sucesso"] is False

    def test_parse_dados_missing_conteudo(self, parser):
        """Test parsing dados with missing conteudo."""
        dados = {
            "codigo": "00",
        }
        
        result = parser._parse_dados(dados)
        
        assert result["codigo"] == "00"
        assert result["sucesso"] is True
        assert result["mensagens"] == []

    def test_parse_dados_with_multiple_messages(self, parser):
        """Test parsing dados with multiple messages."""
        dados = {
            "codigo": "00",
            "conteudo": [
                {
                    "codigoSistemaRemetente": "00014",
                    "codigoModelo": "00009",
                    "assuntoModelo": "Subject 1",
                    "dataEnvio": "20220620",
                },
                {
                    "codigoSistemaRemetente": "00015",
                    "codigoModelo": "00010",
                    "assuntoModelo": "Subject 2",
                    "dataEnvio": "20220621",
                },
            ],
        }
        
        result = parser._parse_dados(dados)
        
        assert len(result["mensagens"]) == 2
        assert result["mensagens"][0]["assunto"] == "Subject 1"
        assert result["mensagens"][1]["assunto"] == "Subject 2"

    def test_parse_full_response(self, parser):
        """Test parsing full response."""
        raw_response = {
            "status": 200,
            "mensagens": [
                {"codigo": "[Sucesso-CAIXAPOSTAL]", "texto": "Requisição efetuada com sucesso."}
            ],
            "contratante": {"numero": "00000000000000", "tipo": 2},
            "autorPedidoDados": {"numero": "00000000000000", "tipo": 2},
            "contribuinte": {"numero": "00000000000000", "tipo": 2},
            "pedidoDados": {
                "idSistema": "CAIXAPOSTAL",
                "idServico": "MSGDETALHAMENTO62",
                "versaoSistema": "1.0",
            },
            "dados": '{"codigo":"00","conteudo":[{"codigoSistemaRemetente":"00014","codigoModelo":"00009","assuntoModelo":"Test Subject","dataEnvio":"20220620"}]}',
        }
        
        result = parser.parse(raw_response)
        
        assert result["status"] == 200
        assert len(result["mensagens"]) == 1
        assert result["mensagens"][0]["codigo"] == "[Sucesso-CAIXAPOSTAL]"
        assert "dados" in result
        assert result["dados"]["codigo"] == "00"
        assert result["dados"]["sucesso"] is True
        assert len(result["dados"]["mensagens"]) == 1
        assert result["dados"]["mensagens"][0]["assunto"] == "Test Subject"

    def test_parse_message_with_missing_fields(self, parser):
        """Test parsing message with missing optional fields."""
        dados = {
            "codigo": "00",
            "conteudo": [
                {
                    "codigoSistemaRemetente": "00014",
                    "codigoModelo": "00009",
                    # Missing many optional fields
                }
            ],
        }
        
        result = parser._parse_dados(dados)
        
        assert len(result["mensagens"]) == 1
        msg = result["mensagens"][0]
        assert msg["codigo_sistema_remetente"] == "00014"
        assert msg["codigo_modelo"] == "00009"
        # Optional fields should be None or empty
        assert msg["assunto"] is None
        assert msg["data_envio"] is None
        assert msg["variaveis"] == []  # Default empty list


class TestInnoVamsg63Template:
    """Tests for InnoVamsg63Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return InnoVamsg63Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "CAIXAPOSTAL"
        assert template.id_servico == "INNOVAMSG63"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Monitorar"

    def test_validate_success_empty_dict(self, template):
        """Test successful validation with empty dictionary."""
        dados = {}
        result = template.validate(dados)
        
        assert result == {}
        assert isinstance(result, dict)
        assert len(result) == 0

    def test_validate_success_empty_string_fields(self, template):
        """Test successful validation with empty string fields."""
        dados = {"field1": "", "field2": "   "}
        result = template.validate(dados)
        
        assert result == {}

    def test_validate_fails_with_data(self, template):
        """Test validation fails when dados contains actual data."""
        dados = {"field": "value"}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "unexpected" in str(exc_info.value).lower() or "does not accept" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999", "tipo": 1}
        
        dados = {}
        request = template.build_request(config, dados)
        
        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request
        
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "CAIXAPOSTAL"
        assert pedido_dados["idServico"] == "INNOVAMSG63"
        assert pedido_dados["versaoSistema"] == "1.0"
        
        # Verify dados is empty string (this service uses empty string, not "{}")
        assert pedido_dados["dados"] == ""

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("CAIXAPOSTAL", "INNOVAMSG63")
        assert template_class is not None
        assert template_class == InnoVamsg63Template


class TestInnoVamsg63ResponseParser:
    """Tests for InnoVamsg63ResponseParser."""

    @pytest.fixture
    def parser(self):
        """Fixture creating a parser instance."""
        return InnoVamsg63ResponseParser()

    def test_init(self, parser):
        """Test parser initialization."""
        assert parser.id_sistema == "CAIXAPOSTAL"
        assert parser.id_servico == "INNOVAMSG63"

    def test_parse_dados_success(self, parser):
        """Test parsing valid dados with indicador - returns original format."""
        dados = {
            "codigo": "00",
            "conteudo": [
                {
                    "indicadorMensagensNovas": "2"
                }
            ],
        }
        
        result = parser._parse_dados(dados)
        
        # Parser returns data in original format (no transformations)
        assert result == dados
        assert result["codigo"] == "00"
        assert "conteudo" in result
        assert result["conteudo"][0]["indicadorMensagensNovas"] == "2"

    def test_parse_dados_error_code(self, parser):
        """Test parsing dados with error code - returns original format."""
        dados = {
            "codigo": "99",
            "conteudo": [
                {
                    "indicadorMensagensNovas": "0"
                }
            ],
        }
        
        result = parser._parse_dados(dados)
        
        # Parser returns data in original format (no transformations)
        assert result == dados
        assert result["codigo"] == "99"
        assert result["conteudo"][0]["indicadorMensagensNovas"] == "0"

    def test_parse_dados_empty_conteudo(self, parser):
        """Test parsing dados with empty conteudo - returns original format."""
        dados = {
            "codigo": "00",
            "conteudo": [],
        }
        
        result = parser._parse_dados(dados)
        
        # Parser returns data in original format (no transformations)
        assert result == dados
        assert result["codigo"] == "00"
        assert result["conteudo"] == []

    def test_parse_dados_missing_conteudo(self, parser):
        """Test parsing dados with missing conteudo - returns original format."""
        dados = {
            "codigo": "00",
        }
        
        result = parser._parse_dados(dados)
        
        # Parser returns data in original format (no transformations)
        assert result == dados
        assert result["codigo"] == "00"

    def test_parse_dados_missing_indicador(self, parser):
        """Test parsing dados with missing indicadorMensagensNovas - returns original format."""
        dados = {
            "codigo": "00",
            "conteudo": [
                {}
            ],
        }
        
        result = parser._parse_dados(dados)
        
        # Parser returns data in original format (no transformations)
        assert result == dados
        assert result["codigo"] == "00"
        assert result["conteudo"] == [{}]

    def test_parse_full_response(self, parser):
        """Test parsing full response - returns original format."""
        raw_response = {
            "status": 200,
            "mensagens": [
                {"codigo": "[Sucesso-CAIXAPOSTAL]", "texto": "Requisição efetuada com sucesso."}
            ],
            "contratante": {"numero": "00000000000000", "tipo": 2},
            "autorPedidoDados": {"numero": "00000000000000", "tipo": 2},
            "contribuinte": {"numero": "99999999999", "tipo": 1},
            "pedidoDados": {
                "idSistema": "CAIXAPOSTAL",
                "idServico": "INNOVAMSG63",
                "versaoSistema": "1.0",
            },
            "dados": '{"codigo":"00","conteudo":[{"indicadorMensagensNovas":"2"}]}',
        }
        
        result = parser.parse(raw_response)
        
        assert result["status"] == 200
        assert len(result["mensagens"]) == 1
        assert result["mensagens"][0]["codigo"] == "[Sucesso-CAIXAPOSTAL]"
        assert "dados" in result
        # Dados should be parsed from JSON string to dict, but in original format
        assert result["dados"]["codigo"] == "00"
        assert "conteudo" in result["dados"]
        assert result["dados"]["conteudo"][0]["indicadorMensagensNovas"] == "2"

    def test_parse_dados_indicador_zero(self, parser):
        """Test parsing dados with indicador zero (no new messages) - returns original format."""
        dados = {
            "codigo": "00",
            "conteudo": [
                {
                    "indicadorMensagensNovas": "0"
                }
            ],
        }
        
        result = parser._parse_dados(dados)
        
        # Parser returns data in original format (no transformations)
        assert result == dados
        assert result["codigo"] == "00"
        assert result["conteudo"][0]["indicadorMensagensNovas"] == "0"


