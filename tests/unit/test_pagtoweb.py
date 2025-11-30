"""Unit tests for PAGTOWEB templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.pagtoweb.consultar import (
    Pagamentos71Template,
    ContaConsDocArrPg73Template,
)
from integra_sdk.templates.pagtoweb.emitir import Comparrecadacao72Template
from integra_sdk.templates.registry import TemplateRegistry


class TestPagamentos71Template:
    """Tests for Pagamentos71Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Pagamentos71Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PAGTOWEB"
        assert template.id_servico == "PAGAMENTOS71"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_by_intervalo_data(self, template):
        """Test validation with intervaloDataArrecadacao."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2019-09-01",
                "dataFinal": "2019-11-30",
            },
            "primeiroDaPagina": 0,
            "tamanhoDaPagina": 100,
        }
        result = template.validate(dados)
        assert "intervaloDataArrecadacao" in result
        assert result["primeiroDaPagina"] == 0
        assert result["tamanhoDaPagina"] == 100

    def test_validate_by_codigo_receita(self, template):
        """Test validation with codigoReceitaLista."""
        dados = {
            "codigoReceitaLista": ["9999", "8888"],
            "primeiroDaPagina": 0,
            "tamanhoDaPagina": 50,
        }
        result = template.validate(dados)
        assert "codigoReceitaLista" in result
        assert result["codigoReceitaLista"] == ["9999", "8888"]

    def test_validate_by_intervalo_valor(self, template):
        """Test validation with intervaloValorTotalDocumento."""
        dados = {
            "intervaloValorTotalDocumento": {
                "valorInicial": 6000,
                "valorFinal": 13000,
            },
        }
        result = template.validate(dados)
        assert "intervaloValorTotalDocumento" in result
        assert result["intervaloValorTotalDocumento"]["valorInicial"] == 6000.0
        assert result["intervaloValorTotalDocumento"]["valorFinal"] == 13000.0

    def test_validate_combined_filters(self, template):
        """Test validation with combined filters."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2022-01-01",
                "dataFinal": "2022-01-31",
            },
            "intervaloValorTotalDocumento": {
                "valorInicial": 6000,
                "valorFinal": 13000,
            },
        }
        result = template.validate(dados)
        assert "intervaloDataArrecadacao" in result
        assert "intervaloValorTotalDocumento" in result

    def test_validate_default_pagination(self, template):
        """Test default pagination values."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2019-09-01",
                "dataFinal": "2019-11-30",
            },
        }
        result = template.validate(dados)
        assert result["primeiroDaPagina"] == 0
        assert result["tamanhoDaPagina"] == 100

    def test_validate_missing_all_filters(self, template):
        """Test validation fails when no filter is provided."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "at least one" in str(exc_info.value).lower()

    def test_validate_invalid_date_format(self, template):
        """Test validation fails with invalid date format."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "01-09-2019",
                "dataFinal": "30-11-2019",
            },
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_validate_empty_codigo_receita_list(self, template):
        """Test validation fails with empty codigoReceitaLista."""
        dados = {"codigoReceitaLista": []}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_invalid_pagination(self, template):
        """Test validation fails with invalid pagination."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2019-09-01",
                "dataFinal": "2019-11-30",
            },
            "tamanhoDaPagina": -1,
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "positive" in str(exc_info.value).lower()

    def test_validate_string_numeric_values(self, template):
        """Test validation accepts string numeric values."""
        dados = {
            "intervaloValorTotalDocumento": {
                "valorInicial": "6000",
                "valorFinal": "13000",
            },
        }
        result = template.validate(dados)
        assert result["intervaloValorTotalDocumento"]["valorInicial"] == 6000.0
        assert result["intervaloValorTotalDocumento"]["valorFinal"] == 13000.0

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}

        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2019-09-01",
                "dataFinal": "2019-11-30",
            },
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PAGTOWEB"
        assert pedido_dados["idServico"] == "PAGAMENTOS71"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PAGTOWEB", "PAGAMENTOS71")
        assert template_class is not None
        assert template_class == Pagamentos71Template


class TestContaConsDocArrPg73Template:
    """Tests for ContaConsDocArrPg73Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ContaConsDocArrPg73Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PAGTOWEB"
        assert template.id_servico == "CONTACONSDOCARRPG73"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_by_intervalo_data(self, template):
        """Test validation with intervaloDataArrecadacao."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2019-09-01",
                "dataFinal": "2019-11-30",
            },
        }
        result = template.validate(dados)
        assert "intervaloDataArrecadacao" in result
        assert result["intervaloDataArrecadacao"]["dataInicial"] == "2019-09-01"
        assert result["intervaloDataArrecadacao"]["dataFinal"] == "2019-11-30"

    def test_validate_by_codigo_receita(self, template):
        """Test validation with codigoReceitaLista."""
        dados = {"codigoReceitaLista": ["9999", "8888"]}
        result = template.validate(dados)
        assert "codigoReceitaLista" in result
        assert result["codigoReceitaLista"] == ["9999", "8888"]

    def test_validate_by_intervalo_valor(self, template):
        """Test validation with intervaloValorTotalDocumento."""
        dados = {
            "intervaloValorTotalDocumento": {
                "valorInicial": 6000,
                "valorFinal": 13000,
            },
        }
        result = template.validate(dados)
        assert "intervaloValorTotalDocumento" in result
        assert result["intervaloValorTotalDocumento"]["valorInicial"] == 6000.0
        assert result["intervaloValorTotalDocumento"]["valorFinal"] == 13000.0

    def test_validate_combined_filters(self, template):
        """Test validation with combined filters."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2022-01-01",
                "dataFinal": "2022-01-31",
            },
            "intervaloValorTotalDocumento": {
                "valorInicial": 6000,
                "valorFinal": 13000,
            },
        }
        result = template.validate(dados)
        assert "intervaloDataArrecadacao" in result
        assert "intervaloValorTotalDocumento" in result

    def test_validate_missing_all_filters(self, template):
        """Test validation fails when no filter is provided."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "at least one" in str(exc_info.value).lower()

    def test_validate_invalid_date_format(self, template):
        """Test validation fails with invalid date format."""
        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "01-09-2019",
                "dataFinal": "30-11-2019",
            },
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_validate_empty_codigo_receita_list(self, template):
        """Test validation fails with empty codigoReceitaLista."""
        dados = {"codigoReceitaLista": []}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_negative_valor(self, template):
        """Test validation fails with negative valor."""
        dados = {
            "intervaloValorTotalDocumento": {
                "valorInicial": -100,
                "valorFinal": 13000,
            },
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "non-negative" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}

        dados = {
            "intervaloDataArrecadacao": {
                "dataInicial": "2019-09-01",
                "dataFinal": "2019-11-30",
            },
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PAGTOWEB"
        assert pedido_dados["idServico"] == "CONTACONSDOCARRPG73"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PAGTOWEB", "CONTACONSDOCARRPG73")
        assert template_class is not None
        assert template_class == ContaConsDocArrPg73Template


class TestComparrecadacao72Template:
    """Tests for Comparrecadacao72Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Comparrecadacao72Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PAGTOWEB"
        assert template.id_servico == "COMPARRECADACAO72"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid numeroDocumento."""
        dados = {"numeroDocumento": "99999999999999999"}
        result = template.validate(dados)
        assert result["numeroDocumento"] == "99999999999999999"

    def test_validate_success_with_whitespace(self, template):
        """Test successful validation with numeroDocumento containing whitespace."""
        dados = {"numeroDocumento": "  99999999999999999  "}
        result = template.validate(dados)
        assert result["numeroDocumento"] == "99999999999999999"

    def test_validate_missing_numero_documento(self, template):
        """Test validation fails when numeroDocumento is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_invalid_numero_documento_type(self, template):
        """Test validation fails when numeroDocumento has invalid type."""
        dados = {"numeroDocumento": 123}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_empty_numero_documento(self, template):
        """Test validation fails when numeroDocumento is empty."""
        dados = {"numeroDocumento": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999", "tipo": 1}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999", "tipo": 1}

        dados = {"numeroDocumento": "99999999999999999"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PAGTOWEB"
        assert pedido_dados["idServico"] == "COMPARRECADACAO72"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PAGTOWEB", "COMPARRECADACAO72")
        assert template_class is not None
        assert template_class == Comparrecadacao72Template

