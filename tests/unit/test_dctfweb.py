"""Unit tests for DCTFWEB templates."""

from unittest.mock import MagicMock

import pytest

import base64

from integra_sdk.exceptions import ValidationError
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
from integra_sdk.templates.registry import TemplateRegistry


class TestGerarGuia31Template:
    """Tests for GerarGuia31Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerarGuia31Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DCTFWEB"
        assert template.id_servico == "GERARGUIA31"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with all required fields."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["categoria"] == "GERAL_MENSAL"
        assert result["anoPA"] == "2027"
        assert result["mesPA"] == "11"
        assert result["numeroReciboEntrega"] == 24573

    def test_validate_success_ano_pa_int(self, template):
        """Test successful validation with anoPA as integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": 2027,
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["anoPA"] == "2027"

    def test_validate_success_mes_pa_int(self, template):
        """Test successful validation with mesPA as integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": 11,
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "11"

    def test_validate_missing_categoria(self, template):
        """Test validation fails when categoria is missing."""
        dados = {
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_missing_ano_pa(self, template):
        """Test validation fails when anoPA is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_missing_mes_pa(self, template):
        """Test validation fails when mesPA is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_missing_numero_recibo_entrega(self, template):
        """Test validation fails when numeroReciboEntrega is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_empty_categoria(self, template):
        """Test validation fails when categoria is empty."""
        dados = {
            "categoria": "",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_whitespace_categoria(self, template):
        """Test validation fails when categoria is only whitespace."""
        dados = {
            "categoria": "   ",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_length(self, template):
        """Test validation fails when anoPA is not 4 digits."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "27",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_non_digit(self, template):
        """Test validation fails when anoPA is not numeric."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "abcd",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_low(self, template):
        """Test validation fails when mesPA is less than 1."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "0",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_high(self, template):
        """Test validation fails when mesPA is greater than 12."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "13",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_non_digit(self, template):
        """Test validation fails when mesPA is not numeric."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "abc",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_zero(self, template):
        """Test validation fails when numeroReciboEntrega is zero."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 0,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_negative(self, template):
        """Test validation fails when numeroReciboEntrega is negative."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": -1,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_type(self, template):
        """Test validation fails when numeroReciboEntrega is not an integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": "24573",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DCTFWEB"
        assert pedido_dados["idServico"] == "GERARGUIA31"
        assert pedido_dados["versaoSistema"] == "1.0"

        # Verify dados is a JSON string
        import json

        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["categoria"] == "GERAL_MENSAL"
        assert dados_parsed["anoPA"] == "2027"
        assert dados_parsed["mesPA"] == "11"
        assert dados_parsed["numeroReciboEntrega"] == 24573

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DCTFWEB", "GERARGUIA31")
        assert template_class is not None
        assert template_class == GerarGuia31Template


class TestConsultarXmlDeclaracao38Template:
    """Tests for ConsultarXmlDeclaracao38Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultarXmlDeclaracao38Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DCTFWEB"
        assert template.id_servico == "CONSXMLDECLARACAO38"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with all required fields."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
        }
        result = template.validate(dados)

        assert result["categoria"] == "PF_MENSAL"
        assert result["anoPA"] == "2022"
        assert result["mesPA"] == "06"

    def test_validate_success_mes_single_digit(self, template):
        """Test successful validation with single-digit month (should be zero-padded)."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "6",
        }
        result = template.validate(dados)

        assert result["mesPA"] == "06"

    def test_validate_success_ano_pa_int(self, template):
        """Test successful validation with anoPA as integer."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": 2022,
            "mesPA": "06",
        }
        result = template.validate(dados)

        assert result["anoPA"] == "2022"

    def test_validate_success_mes_pa_int(self, template):
        """Test successful validation with mesPA as integer."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": 6,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "06"

    def test_validate_missing_categoria(self, template):
        """Test validation fails when categoria is missing."""
        dados = {
            "anoPA": "2022",
            "mesPA": "06",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_missing_ano_pa(self, template):
        """Test validation fails when anoPA is missing."""
        dados = {
            "categoria": "PF_MENSAL",
            "mesPA": "06",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_missing_mes_pa(self, template):
        """Test validation fails when mesPA is missing."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_empty_categoria(self, template):
        """Test validation fails when categoria is empty."""
        dados = {
            "categoria": "",
            "anoPA": "2022",
            "mesPA": "06",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_whitespace_categoria(self, template):
        """Test validation fails when categoria is only whitespace."""
        dados = {
            "categoria": "   ",
            "anoPA": "2022",
            "mesPA": "06",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_length(self, template):
        """Test validation fails when anoPA is not 4 digits."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "22",
            "mesPA": "06",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_non_digit(self, template):
        """Test validation fails when anoPA is not numeric."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "abcd",
            "mesPA": "06",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_low(self, template):
        """Test validation fails when mesPA is less than 1."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "0",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_high(self, template):
        """Test validation fails when mesPA is greater than 12."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "13",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_non_digit(self, template):
        """Test validation fails when mesPA is not numeric."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "abc",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000", "tipo": 1}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000", "tipo": 1}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000", "tipo": 1}

        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
        }
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DCTFWEB"
        assert pedido_dados["idServico"] == "CONSXMLDECLARACAO38"
        assert pedido_dados["versaoSistema"] == "1.0"

        # Verify dados is a JSON string
        import json

        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["categoria"] == "PF_MENSAL"
        assert dados_parsed["anoPA"] == "2022"
        assert dados_parsed["mesPA"] == "06"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DCTFWEB", "CONSXMLDECLARACAO38")
        assert template_class is not None
        assert template_class == ConsultarXmlDeclaracao38Template


class TestConsultarRecibo32Template:
    """Tests for ConsultarRecibo32Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultarRecibo32Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DCTFWEB"
        assert template.id_servico == "CONSRECIBO32"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with all required fields."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["categoria"] == 40
        assert result["anoPA"] == "2027"
        assert result["mesPA"] == "11"
        assert result["numeroReciboEntrega"] == 24573

    def test_validate_success_mes_single_digit(self, template):
        """Test successful validation with single-digit month (should be zero-padded)."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "6",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "06"

    def test_validate_success_ano_pa_int(self, template):
        """Test successful validation with anoPA as integer."""
        dados = {
            "categoria": 40,
            "anoPA": 2027,
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["anoPA"] == "2027"

    def test_validate_success_mes_pa_int(self, template):
        """Test successful validation with mesPA as integer."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": 11,
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "11"

    def test_validate_missing_categoria(self, template):
        """Test validation fails when categoria is missing."""
        dados = {
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_missing_ano_pa(self, template):
        """Test validation fails when anoPA is missing."""
        dados = {
            "categoria": 40,
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_missing_mes_pa(self, template):
        """Test validation fails when mesPA is missing."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_missing_numero_recibo_entrega(self, template):
        """Test validation fails when numeroReciboEntrega is missing."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "11",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_invalid_categoria_type_string(self, template):
        """Test validation fails when categoria is a string."""
        dados = {
            "categoria": "40",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_categoria_zero(self, template):
        """Test validation fails when categoria is zero."""
        dados = {
            "categoria": 0,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_categoria_negative(self, template):
        """Test validation fails when categoria is negative."""
        dados = {
            "categoria": -1,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_length(self, template):
        """Test validation fails when anoPA is not 4 digits."""
        dados = {
            "categoria": 40,
            "anoPA": "27",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_non_digit(self, template):
        """Test validation fails when anoPA is not numeric."""
        dados = {
            "categoria": 40,
            "anoPA": "abcd",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_low(self, template):
        """Test validation fails when mesPA is less than 1."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "0",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_high(self, template):
        """Test validation fails when mesPA is greater than 12."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "13",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_zero(self, template):
        """Test validation fails when numeroReciboEntrega is zero."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 0,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_negative(self, template):
        """Test validation fails when numeroReciboEntrega is negative."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": -1,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_type(self, template):
        """Test validation fails when numeroReciboEntrega is not an integer."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": "24573",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DCTFWEB"
        assert pedido_dados["idServico"] == "CONSRECIBO32"
        assert pedido_dados["versaoSistema"] == "1.0"

        # Verify dados is a JSON string
        import json

        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["categoria"] == 40
        assert dados_parsed["anoPA"] == "2027"
        assert dados_parsed["mesPA"] == "11"
        assert dados_parsed["numeroReciboEntrega"] == 24573

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DCTFWEB", "CONSRECIBO32")
        assert template_class is not None
        assert template_class == ConsultarRecibo32Template


class TestConsultarRelatorioCompleta33Template:
    """Tests for ConsultarRelatorioCompleta33Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultarRelatorioCompleta33Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DCTFWEB"
        assert template.id_servico == "CONSDECCOMPLETA33"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with all required fields."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["categoria"] == "GERAL_MENSAL"
        assert result["anoPA"] == "2027"
        assert result["mesPA"] == "11"
        assert result["numeroReciboEntrega"] == 24573

    def test_validate_success_mes_single_digit(self, template):
        """Test successful validation with single-digit month (should be zero-padded)."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "6",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "06"

    def test_validate_success_ano_pa_int(self, template):
        """Test successful validation with anoPA as integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": 2027,
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["anoPA"] == "2027"

    def test_validate_success_mes_pa_int(self, template):
        """Test successful validation with mesPA as integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": 11,
            "numeroReciboEntrega": 24573,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "11"

    def test_validate_missing_categoria(self, template):
        """Test validation fails when categoria is missing."""
        dados = {
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_missing_ano_pa(self, template):
        """Test validation fails when anoPA is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_missing_mes_pa(self, template):
        """Test validation fails when mesPA is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_missing_numero_recibo_entrega(self, template):
        """Test validation fails when numeroReciboEntrega is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_empty_categoria(self, template):
        """Test validation fails when categoria is empty."""
        dados = {
            "categoria": "",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_whitespace_categoria(self, template):
        """Test validation fails when categoria is only whitespace."""
        dados = {
            "categoria": "   ",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_categoria_type(self, template):
        """Test validation fails when categoria is not a string."""
        dados = {
            "categoria": 40,
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_length(self, template):
        """Test validation fails when anoPA is not 4 digits."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "27",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_non_digit(self, template):
        """Test validation fails when anoPA is not numeric."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "abcd",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_low(self, template):
        """Test validation fails when mesPA is less than 1."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "0",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_high(self, template):
        """Test validation fails when mesPA is greater than 12."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "13",
            "numeroReciboEntrega": 24573,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_zero(self, template):
        """Test validation fails when numeroReciboEntrega is zero."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 0,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_negative(self, template):
        """Test validation fails when numeroReciboEntrega is negative."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": -1,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_validate_invalid_numero_recibo_entrega_type(self, template):
        """Test validation fails when numeroReciboEntrega is not an integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": "24573",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "numeroreciboentrega" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2027",
            "mesPA": "11",
            "numeroReciboEntrega": 24573,
        }
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DCTFWEB"
        assert pedido_dados["idServico"] == "CONSDECCOMPLETA33"
        assert pedido_dados["versaoSistema"] == "1.0"

        # Verify dados is a JSON string
        import json

        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["categoria"] == "GERAL_MENSAL"
        assert dados_parsed["anoPA"] == "2027"
        assert dados_parsed["mesPA"] == "11"
        assert dados_parsed["numeroReciboEntrega"] == 24573

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DCTFWEB", "CONSDECCOMPLETA33")
        assert template_class is not None
        assert template_class == ConsultarRelatorioCompleta33Template


class TestGerarGuiaAndamento313Template:
    """Tests for GerarGuiaAndamento313Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerarGuiaAndamento313Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DCTFWEB"
        assert template.id_servico == "GERARGUIAANDAMENTO313"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with all required fields."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
            "mesPA": "01",
        }
        result = template.validate(dados)

        assert result["categoria"] == "GERAL_MENSAL"
        assert result["anoPA"] == "2025"
        assert result["mesPA"] == "01"

    def test_validate_success_mes_single_digit(self, template):
        """Test successful validation with single-digit month (should be zero-padded)."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
            "mesPA": "6",
        }
        result = template.validate(dados)

        assert result["mesPA"] == "06"

    def test_validate_success_ano_pa_int(self, template):
        """Test successful validation with anoPA as integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": 2025,
            "mesPA": "01",
        }
        result = template.validate(dados)

        assert result["anoPA"] == "2025"

    def test_validate_success_mes_pa_int(self, template):
        """Test successful validation with mesPA as integer."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
            "mesPA": 1,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "01"

    def test_validate_missing_categoria(self, template):
        """Test validation fails when categoria is missing."""
        dados = {
            "anoPA": "2025",
            "mesPA": "01",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_missing_ano_pa(self, template):
        """Test validation fails when anoPA is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "mesPA": "01",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_missing_mes_pa(self, template):
        """Test validation fails when mesPA is missing."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_empty_categoria(self, template):
        """Test validation fails when categoria is empty."""
        dados = {
            "categoria": "",
            "anoPA": "2025",
            "mesPA": "01",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_whitespace_categoria(self, template):
        """Test validation fails when categoria is only whitespace."""
        dados = {
            "categoria": "   ",
            "anoPA": "2025",
            "mesPA": "01",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_categoria_type(self, template):
        """Test validation fails when categoria is not a string."""
        dados = {
            "categoria": 40,
            "anoPA": "2025",
            "mesPA": "01",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_length(self, template):
        """Test validation fails when anoPA is not 4 digits."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "25",
            "mesPA": "01",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_non_digit(self, template):
        """Test validation fails when anoPA is not numeric."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "abcd",
            "mesPA": "01",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_low(self, template):
        """Test validation fails when mesPA is less than 1."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
            "mesPA": "0",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_high(self, template):
        """Test validation fails when mesPA is greater than 12."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
            "mesPA": "13",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_non_digit(self, template):
        """Test validation fails when mesPA is not numeric."""
        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
            "mesPA": "abc",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "categoria": "GERAL_MENSAL",
            "anoPA": "2025",
            "mesPA": "01",
        }
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DCTFWEB"
        assert pedido_dados["idServico"] == "GERARGUIAANDAMENTO313"
        assert pedido_dados["versaoSistema"] == "1.0"

        # Verify dados is a JSON string
        import json

        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["categoria"] == "GERAL_MENSAL"
        assert dados_parsed["anoPA"] == "2025"
        assert dados_parsed["mesPA"] == "01"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DCTFWEB", "GERARGUIAANDAMENTO313")
        assert template_class is not None
        assert template_class == GerarGuiaAndamento313Template


class TestTransmitirDeclaracao310Template:
    """Tests for TransmitirDeclaracao310Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return TransmitirDeclaracao310Template()

    @pytest.fixture
    def valid_xml_base64(self):
        """Fixture with valid base64 encoded XML."""
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
<ProcDctf xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.serpro.gov.br/dctf/v1">
    <ConteudoDeclaracao id="id_16436">
        <tns1:DctfXml xsi:type="DctfXml_v3" versao="3.0" xmlns:tns1="http://www.serpro.gov.br/dctf/v1" xmlns="http://www.serpro.gov.br/dctf/v1" type="DctfXml_v3">
            <A000-DadosIdentificadoresContribuinte>
                <nomeContribuinte>TEST XML</nomeContribuinte>
            </A000-DadosIdentificadoresContribuinte>
        </tns1:DctfXml>
    </ConteudoDeclaracao>
</ProcDctf>"""
        return base64.b64encode(xml_content.encode("utf-8")).decode("utf-8")

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DCTFWEB"
        assert template.id_servico == "TRANSDECLARACAO310"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Transmitir"

    def test_validate_success(self, template, valid_xml_base64):
        """Test successful validation with all required fields."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }
        result = template.validate(dados)

        assert result["categoria"] == "PF_MENSAL"
        assert result["anoPA"] == "2022"
        assert result["mesPA"] == "06"
        assert result["xmlAssinadoBase64"] == valid_xml_base64

    def test_validate_success_mes_single_digit(self, template, valid_xml_base64):
        """Test successful validation with single-digit month (should be zero-padded)."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "6",
            "xmlAssinadoBase64": valid_xml_base64,
        }
        result = template.validate(dados)

        assert result["mesPA"] == "06"

    def test_validate_missing_categoria(self, template, valid_xml_base64):
        """Test validation fails when categoria is missing."""
        dados = {
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_missing_ano_pa(self, template, valid_xml_base64):
        """Test validation fails when anoPA is missing."""
        dados = {
            "categoria": "PF_MENSAL",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_missing_mes_pa(self, template, valid_xml_base64):
        """Test validation fails when mesPA is missing."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_missing_xml_assinado_base64(self, template):
        """Test validation fails when xmlAssinadoBase64 is missing."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "xmlassinadobase64" in str(exc_info.value).lower()

    def test_validate_empty_categoria(self, template, valid_xml_base64):
        """Test validation fails when categoria is empty."""
        dados = {
            "categoria": "",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_whitespace_categoria(self, template, valid_xml_base64):
        """Test validation fails when categoria is only whitespace."""
        dados = {
            "categoria": "   ",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_categoria_type(self, template, valid_xml_base64):
        """Test validation fails when categoria is not a string."""
        dados = {
            "categoria": 123,
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "categoria" in str(exc_info.value).lower()

    def test_validate_invalid_ano_pa_length(self, template, valid_xml_base64):
        """Test validation fails when anoPA is not 4 digits."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "22",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "anopa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_low(self, template, valid_xml_base64):
        """Test validation fails when mesPA is less than 1."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "0",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_invalid_mes_pa_high(self, template, valid_xml_base64):
        """Test validation fails when mesPA is greater than 12."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "13",
            "xmlAssinadoBase64": valid_xml_base64,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "mespa" in str(exc_info.value).lower()

    def test_validate_empty_xml_assinado_base64(self, template):
        """Test validation fails when xmlAssinadoBase64 is empty."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": "",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "xmlassinadobase64" in str(exc_info.value).lower()

    def test_validate_whitespace_xml_assinado_base64(self, template):
        """Test validation fails when xmlAssinadoBase64 is only whitespace."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": "   ",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "xmlassinadobase64" in str(exc_info.value).lower()

    def test_validate_invalid_xml_assinado_base64_type(self, template):
        """Test validation fails when xmlAssinadoBase64 is not a string."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": 12345,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "xmlassinadobase64" in str(exc_info.value).lower()

    def test_validate_invalid_xml_assinado_base64_not_base64(self, template):
        """Test validation fails when xmlAssinadoBase64 is not valid Base64."""
        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": "not-valid-base64!!!",
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "xmlassinadobase64" in str(exc_info.value).lower()
        assert "base64" in str(exc_info.value).lower()

    def test_build_request(self, template, valid_xml_base64):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000", "tipo": 1}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000", "tipo": 1}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000", "tipo": 1}

        dados = {
            "categoria": "PF_MENSAL",
            "anoPA": "2022",
            "mesPA": "06",
            "xmlAssinadoBase64": valid_xml_base64,
        }
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DCTFWEB"
        assert pedido_dados["idServico"] == "TRANSDECLARACAO310"
        assert pedido_dados["versaoSistema"] == "1.0"

        # Verify dados is a JSON string
        import json

        dados_parsed = json.loads(pedido_dados["dados"])
        assert dados_parsed["categoria"] == "PF_MENSAL"
        assert dados_parsed["anoPA"] == "2022"
        assert dados_parsed["mesPA"] == "06"
        assert dados_parsed["xmlAssinadoBase64"] == valid_xml_base64

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DCTFWEB", "TRANSDECLARACAO310")
        assert template_class is not None
        assert template_class == TransmitirDeclaracao310Template

