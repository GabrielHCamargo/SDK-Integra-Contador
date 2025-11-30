"""Unit tests for PGMEI templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.pgmei.emitir import (
    GerardasPdf21Template,
    GerardasCodBarra22Template,
    AtuBeneficio23Template,
)
from integra_sdk.templates.pgmei.consultar import ConsDividaAtiva24Template
from integra_sdk.templates.registry import TemplateRegistry


class TestGerardasPdf21Template:
    """Tests for GerardasPdf21Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerardasPdf21Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGMEI"
        assert template.id_servico == "GERARDASPDF21"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid periodoApuracao."""
        dados = {"periodoApuracao": "201901"}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201901"

    def test_validate_periodo_as_int(self, template):
        """Test validation accepts periodoApuracao as int and converts to string."""
        dados = {"periodoApuracao": 201901}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201901"

    def test_validate_missing_periodo(self, template):
        """Test validation fails when periodoApuracao is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "periodo" in str(exc_info.value).lower()

    def test_validate_invalid_format(self, template):
        """Test validation fails with invalid periodoApuracao format."""
        dados = {"periodoApuracao": "1901"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"periodoApuracao": "201901"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGMEI"
        assert pedido_dados["idServico"] == "GERARDASPDF21"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGMEI", "GERARDASPDF21")
        assert template_class is not None
        assert template_class == GerardasPdf21Template


class TestGerardasCodBarra22Template:
    """Tests for GerardasCodBarra22Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerardasCodBarra22Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGMEI"
        assert template.id_servico == "GERARDASCODBARRA22"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid periodoApuracao."""
        dados = {"periodoApuracao": "201901"}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201901"

    def test_validate_periodo_as_int(self, template):
        """Test validation accepts periodoApuracao as int and converts to string."""
        dados = {"periodoApuracao": 201901}
        result = template.validate(dados)
        assert result["periodoApuracao"] == "201901"

    def test_validate_missing_periodo(self, template):
        """Test validation fails when periodoApuracao is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "periodo" in str(exc_info.value).lower()

    def test_validate_invalid_format(self, template):
        """Test validation fails with invalid periodoApuracao format."""
        dados = {"periodoApuracao": "1901"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"periodoApuracao": "201901"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGMEI"
        assert pedido_dados["idServico"] == "GERARDASCODBARRA22"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGMEI", "GERARDASCODBARRA22")
        assert template_class is not None
        assert template_class == GerardasCodBarra22Template


class TestAtuBeneficio23Template:
    """Tests for AtuBeneficio23Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return AtuBeneficio23Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGMEI"
        assert template.id_servico == "ATUBENEFICIO23"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {
            "anoCalendario": 2021,
            "infoBeneficio": [
                {"periodoApuracao": "202101", "indicadorBeneficio": True},
                {"periodoApuracao": "202102", "indicadorBeneficio": True},
            ],
        }
        result = template.validate(dados)
        assert result["anoCalendario"] == 2021
        assert len(result["infoBeneficio"]) == 2

    def test_validate_ano_as_string(self, template):
        """Test validation accepts anoCalendario as string and converts to int."""
        dados = {
            "anoCalendario": "2021",
            "infoBeneficio": [{"periodoApuracao": "202101", "indicadorBeneficio": True}],
        }
        result = template.validate(dados)
        assert result["anoCalendario"] == 2021

    def test_validate_missing_ano(self, template):
        """Test validation fails when anoCalendario is missing."""
        dados = {"infoBeneficio": []}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_missing_info(self, template):
        """Test validation fails when infoBeneficio is missing."""
        dados = {"anoCalendario": 2021}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "info" in str(exc_info.value).lower()

    def test_validate_empty_info(self, template):
        """Test validation fails when infoBeneficio is empty."""
        dados = {"anoCalendario": 2021, "infoBeneficio": []}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_invalid_ano_range(self, template):
        """Test validation fails with year out of range."""
        dados = {"anoCalendario": 1800, "infoBeneficio": [{"periodoApuracao": "202101"}]}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "year" in str(exc_info.value).lower() or "1900" in str(exc_info.value)

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "anoCalendario": 2021,
            "infoBeneficio": [{"periodoApuracao": "202101", "indicadorBeneficio": True}],
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGMEI"
        assert pedido_dados["idServico"] == "ATUBENEFICIO23"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGMEI", "ATUBENEFICIO23")
        assert template_class is not None
        assert template_class == AtuBeneficio23Template


class TestConsDividaAtiva24Template:
    """Tests for ConsDividaAtiva24Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsDividaAtiva24Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PGMEI"
        assert template.id_servico == "DIVIDAATIVA24"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid anoCalendario."""
        dados = {"anoCalendario": "2020"}
        result = template.validate(dados)
        assert result["anoCalendario"] == "2020"

    def test_validate_ano_as_int(self, template):
        """Test validation accepts anoCalendario as int and converts to string."""
        dados = {"anoCalendario": 2020}
        result = template.validate(dados)
        assert result["anoCalendario"] == "2020"

    def test_validate_missing_ano(self, template):
        """Test validation fails when anoCalendario is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_format(self, template):
        """Test validation fails with invalid anoCalendario format."""
        dados = {"anoCalendario": "20"}
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

        dados = {"anoCalendario": "2020"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PGMEI"
        assert pedido_dados["idServico"] == "DIVIDAATIVA24"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PGMEI", "DIVIDAATIVA24")
        assert template_class is not None
        assert template_class == ConsDividaAtiva24Template


