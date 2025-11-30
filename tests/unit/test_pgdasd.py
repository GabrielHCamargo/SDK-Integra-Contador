"""Unit tests for PGDAS-D templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.pgdasd.consultar import (
    ConsDeclaracao13Template,
    ConsultimaDecRec14Template,
    ConsDecRec15Template,
    ConsExtrato16Template,
)
from integra_sdk.templates.pgdasd.emitir import (
    Gerardas12Template,
    GerardasAvulso19Template,
    GerardasCobranca17Template,
    GerardasProcesso18Template,
)
from integra_sdk.templates.pgdasd.declarar import TransDeclaracao11Template
from integra_sdk.templates.registry import TemplateRegistry


class TestConsDeclaracao13Template:
    """Tests for ConsDeclaracao13Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsDeclaracao13Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "CONSDECLARACAO13"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid anoCalendario."""
        dados = {"anoCalendario": "2018"}
        result = template.validate(dados)
        assert result["anoCalendario"] == "2018"

    def test_validate_ano_as_int(self, template):
        """Test validation accepts anoCalendario as int and converts to string."""
        dados = {"anoCalendario": 2018}
        result = template.validate(dados)
        assert result["anoCalendario"] == "2018"

    def test_validate_missing_ano(self, template):
        """Test validation fails when anoCalendario is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_format(self, template):
        """Test validation fails with invalid anoCalendario format."""
        dados = {"anoCalendario": "18"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_validate_invalid_year_range(self, template):
        """Test validation fails with year out of range."""
        dados = {"anoCalendario": "1800"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "year" in str(exc_info.value).lower() or "1900" in str(exc_info.value)

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"anoCalendario": "2018"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "CONSDECLARACAO13"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "CONSDECLARACAO13")
        assert template_class is not None
        assert template_class == ConsDeclaracao13Template


class TestGerardas12Template:
    """Tests for Gerardas12Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Gerardas12Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "GERARDAS12"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid periodoApuracao."""
        dados = {"periodoApuracao": "201801"}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201801"

    def test_validate_periodo_as_int(self, template):
        """Test validation accepts periodoApuracao as int and converts to string."""
        dados = {"periodoApuracao": 201801}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201801"

    def test_validate_missing_periodo(self, template):
        """Test validation fails when periodoApuracao is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "periodo" in str(exc_info.value).lower()

    def test_validate_invalid_format(self, template):
        """Test validation fails with invalid periodoApuracao format."""
        dados = {"periodoApuracao": "1801"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"periodoApuracao": "201801"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "GERARDAS12"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "GERARDAS12")
        assert template_class is not None
        assert template_class == Gerardas12Template


class TestConsultimaDecRec14Template:
    """Tests for ConsultimaDecRec14Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultimaDecRec14Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "CONSULTIMADECREC14"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid periodoApuracao."""
        dados = {"periodoApuracao": "201801"}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201801"

    def test_validate_periodo_as_int(self, template):
        """Test validation accepts periodoApuracao as int and converts to string."""
        dados = {"periodoApuracao": 201801}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201801"

    def test_validate_missing_periodo(self, template):
        """Test validation fails when periodoApuracao is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "periodo" in str(exc_info.value).lower()

    def test_validate_invalid_format(self, template):
        """Test validation fails with invalid periodoApuracao format."""
        dados = {"periodoApuracao": "1801"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"periodoApuracao": "201801"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "CONSULTIMADECREC14"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "CONSULTIMADECREC14")
        assert template_class is not None
        assert template_class == ConsultimaDecRec14Template


class TestConsDecRec15Template:
    """Tests for ConsDecRec15Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsDecRec15Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "CONSDECREC15"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid numeroDeclaracao."""
        dados = {"numeroDeclaracao": "00000000201801001"}
        result = template.validate(dados)
        assert result["numeroDeclaracao"] == "00000000201801001"

    def test_validate_numero_as_int(self, template):
        """Test validation accepts numeroDeclaracao as int and converts to string."""
        dados = {"numeroDeclaracao": 201801001}
        result = template.validate(dados)
        assert result["numeroDeclaracao"] == "201801001"

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroDeclaracao is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_empty_numero(self, template):
        """Test validation fails when numeroDeclaracao is empty."""
        dados = {"numeroDeclaracao": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroDeclaracao": "00000000201801001"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "CONSDECREC15"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "CONSDECREC15")
        assert template_class is not None
        assert template_class == ConsDecRec15Template


class TestConsExtrato16Template:
    """Tests for ConsExtrato16Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsExtrato16Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "CONSEXTRATO16"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid numeroDas."""
        dados = {"numeroDas": "07202136999997159"}
        result = template.validate(dados)
        assert result["numeroDas"] == "07202136999997159"

    def test_validate_numero_as_int(self, template):
        """Test validation accepts numeroDas as int and converts to string."""
        dados = {"numeroDas": 7202136999997159}
        result = template.validate(dados)
        assert result["numeroDas"] == "7202136999997159"

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroDas is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_empty_numero(self, template):
        """Test validation fails when numeroDas is empty."""
        dados = {"numeroDas": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroDas": "07202136999997159"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "CONSEXTRATO16"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "CONSEXTRATO16")
        assert template_class is not None
        assert template_class == ConsExtrato16Template


class TestTransDeclaracao11Template:
    """Tests for TransDeclaracao11Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return TransDeclaracao11Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "TRANSDECLARACAO11"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Declarar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"cnpjCompleto": "00000000000100", "pa": 202101}
        result = template.validate(dados)
        assert result == dados

    def test_validate_empty_dict(self, template):
        """Test validation fails when dados is empty."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_not_dict(self, template):
        """Test validation fails when dados is not a dict."""
        dados = "not a dict"
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "dictionary" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"cnpjCompleto": "00000000000100", "pa": 202101}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "TRANSDECLARACAO11"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "TRANSDECLARACAO11")
        assert template_class is not None
        assert template_class == TransDeclaracao11Template


class TestGerardasAvulso19Template:
    """Tests for GerardasAvulso19Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerardasAvulso19Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "GERARDASAVULSO19"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {
            "PeriodoApuracao": 202401,
            "ListaTributos": [
                {"Codigo": 1010, "Valor": 111.22, "CodMunicipio": 375, "uf": "PA"},
                {"Codigo": 1007, "Valor": 20.50, "uf": "RJ"},
            ],
        }
        result = template.validate(dados)
        assert result["PeriodoApuracao"] == 202401
        assert len(result["ListaTributos"]) == 2

    def test_validate_periodo_as_string(self, template):
        """Test validation accepts PeriodoApuracao as string and converts to int."""
        dados = {
            "PeriodoApuracao": "202401",
            "ListaTributos": [{"Codigo": 1010, "Valor": 111.22}],
        }
        result = template.validate(dados)
        assert result["PeriodoApuracao"] == 202401

    def test_validate_missing_periodo(self, template):
        """Test validation fails when PeriodoApuracao is missing."""
        dados = {"ListaTributos": []}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "periodo" in str(exc_info.value).lower()

    def test_validate_missing_lista(self, template):
        """Test validation fails when ListaTributos is missing."""
        dados = {"PeriodoApuracao": 202401}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "lista" in str(exc_info.value).lower()

    def test_validate_empty_lista(self, template):
        """Test validation fails when ListaTributos is empty."""
        dados = {"PeriodoApuracao": 202401, "ListaTributos": []}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_invalid_periodo_format(self, template):
        """Test validation fails with invalid PeriodoApuracao format."""
        dados = {"PeriodoApuracao": 180000, "ListaTributos": [{"Codigo": 1010}]}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "PeriodoApuracao": 202401,
            "ListaTributos": [{"Codigo": 1010, "Valor": 111.22}],
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "GERARDASAVULSO19"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "GERARDASAVULSO19")
        assert template_class is not None
        assert template_class == GerardasAvulso19Template


class TestGerardasCobranca17Template:
    """Tests for GerardasCobranca17Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerardasCobranca17Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "GERARDASCOBRANCA17"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid periodoApuracao."""
        dados = {"periodoApuracao": "202301"}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "202301"

    def test_validate_periodo_as_int(self, template):
        """Test validation accepts periodoApuracao as int and converts to string."""
        dados = {"periodoApuracao": 202301}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "202301"

    def test_validate_missing_periodo(self, template):
        """Test validation fails when periodoApuracao is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "periodo" in str(exc_info.value).lower()

    def test_validate_invalid_format(self, template):
        """Test validation fails with invalid periodoApuracao format."""
        dados = {"periodoApuracao": "2301"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"periodoApuracao": "202301"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "GERARDASCOBRANCA17"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "GERARDASCOBRANCA17")
        assert template_class is not None
        assert template_class == GerardasCobranca17Template


class TestGerardasProcesso18Template:
    """Tests for GerardasProcesso18Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerardasProcesso18Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGDASD"
        assert template.id_servico == "GERARDASPROCESSO18"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid numeroProcesso."""
        dados = {"numeroProcesso": "00000000000000000"}
        result = template.validate(dados)
        assert result["numeroProcesso"] == "00000000000000000"

    def test_validate_numero_as_int(self, template):
        """Test validation accepts numeroProcesso as int and converts to string."""
        dados = {"numeroProcesso": 12345678901234567}
        result = template.validate(dados)
        assert result["numeroProcesso"] == "12345678901234567"

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroProcesso is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_empty_numero(self, template):
        """Test validation fails when numeroProcesso is empty."""
        dados = {"numeroProcesso": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroProcesso": "00000000000000000"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGDASD"
        assert pedido_dados["idServico"] == "GERARDASPROCESSO18"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGDASD", "GERARDASPROCESSO18")
        assert template_class is not None
        assert template_class == GerardasProcesso18Template


