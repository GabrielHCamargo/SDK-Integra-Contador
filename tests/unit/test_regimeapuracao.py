"""Unit tests for REGIME APURACAO templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.regimeapuracao.consultar import (
    ConsultarAnosCalendarios102Template,
    ConsultarOpcaoRegime103Template,
    ConsultarResolucao104Template,
)
from integra_sdk.templates.regimeapuracao.declarar import EfetuarOpcaoRegime101Template
from integra_sdk.templates.registry import TemplateRegistry


class TestEfetuarOpcaoRegime101Template:
    """Tests for EfetuarOpcaoRegime101Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return EfetuarOpcaoRegime101Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "REGIMEAPURACAO"
        assert template.id_servico == "EFETUAROPCAOREGIME101"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Declarar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {
            "anoOpcao": 2023,
            "tipoRegime": 1,
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": True,
        }
        result = template.validate(dados)
        assert result["anoOpcao"] == 2023
        assert result["tipoRegime"] == 1
        assert result["descritivoRegime"] == "CAIXA"
        assert result["deAcordoResolucao"] is True

    def test_validate_ano_as_string(self, template):
        """Test validation accepts anoOpcao as string and converts to int."""
        dados = {
            "anoOpcao": "2023",
            "tipoRegime": 1,
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": True,
        }
        result = template.validate(dados)
        assert result["anoOpcao"] == 2023

    def test_validate_tipo_as_string(self, template):
        """Test validation accepts tipoRegime as string and converts to int."""
        dados = {
            "anoOpcao": 2023,
            "tipoRegime": "1",
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": True,
        }
        result = template.validate(dados)
        assert result["tipoRegime"] == 1

    def test_validate_missing_ano(self, template):
        """Test validation fails when anoOpcao is missing."""
        dados = {
            "tipoRegime": 1,
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": True,
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_missing_tipo(self, template):
        """Test validation fails when tipoRegime is missing."""
        dados = {
            "anoOpcao": 2023,
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": True,
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "tipo" in str(exc_info.value).lower()

    def test_validate_missing_descritivo(self, template):
        """Test validation fails when descritivoRegime is missing."""
        dados = {
            "anoOpcao": 2023,
            "tipoRegime": 1,
            "deAcordoResolucao": True,
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "descritivo" in str(exc_info.value).lower()

    def test_validate_missing_acordo(self, template):
        """Test validation fails when deAcordoResolucao is missing."""
        dados = {
            "anoOpcao": 2023,
            "tipoRegime": 1,
            "descritivoRegime": "CAIXA",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "acordo" in str(exc_info.value).lower()

    def test_validate_empty_descritivo(self, template):
        """Test validation fails when descritivoRegime is empty."""
        dados = {
            "anoOpcao": 2023,
            "tipoRegime": 1,
            "descritivoRegime": "",
            "deAcordoResolucao": True,
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_invalid_ano_range(self, template):
        """Test validation fails with year out of range."""
        dados = {
            "anoOpcao": 1800,
            "tipoRegime": 1,
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": True,
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "year" in str(exc_info.value).lower() or "1900" in str(exc_info.value)

    def test_validate_acordo_as_string(self, template):
        """Test validation accepts deAcordoResolucao as string and converts to bool."""
        dados = {
            "anoOpcao": 2023,
            "tipoRegime": 1,
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": "true",
        }
        result = template.validate(dados)
        assert result["deAcordoResolucao"] is True

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "anoOpcao": 2023,
            "tipoRegime": 1,
            "descritivoRegime": "CAIXA",
            "deAcordoResolucao": True,
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "REGIMEAPURACAO"
        assert pedido_dados["idServico"] == "EFETUAROPCAOREGIME101"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("REGIMEAPURACAO", "EFETUAROPCAOREGIME101")
        assert template_class is not None
        assert template_class == EfetuarOpcaoRegime101Template


class TestConsultarAnosCalendarios102Template:
    """Tests for ConsultarAnosCalendarios102Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultarAnosCalendarios102Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "REGIMEAPURACAO"
        assert template.id_servico == "CONSULTARANOSCALENDARIOS102"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with empty dados."""
        dados = {}
        result = template.validate(dados)
        assert result == {}

    def test_validate_fails_with_data(self, template):
        """Test validation fails when dados is not empty."""
        dados = {"some": "data"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_serialize_dados(self, template):
        """Test dados serialization returns empty string."""
        dados = {}
        result = template._serialize_dados(dados)
        assert result == ""

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "REGIMEAPURACAO"
        assert pedido_dados["idServico"] == "CONSULTARANOSCALENDARIOS102"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("REGIMEAPURACAO", "CONSULTARANOSCALENDARIOS102")
        assert template_class is not None
        assert template_class == ConsultarAnosCalendarios102Template


class TestConsultarOpcaoRegime103Template:
    """Tests for ConsultarOpcaoRegime103Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultarOpcaoRegime103Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "REGIMEAPURACAO"
        assert template.id_servico == "CONSULTAROPCAOREGIME103"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid anoCalendario."""
        dados = {"anoCalendario": 2023}
        result = template.validate(dados)
        assert result["anoCalendario"] == 2023

    def test_validate_ano_as_string(self, template):
        """Test validation accepts anoCalendario as string and converts to int."""
        dados = {"anoCalendario": "2023"}
        result = template.validate(dados)
        assert result["anoCalendario"] == 2023

    def test_validate_missing_ano(self, template):
        """Test validation fails when anoCalendario is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_year_range(self, template):
        """Test validation fails with year out of range."""
        dados = {"anoCalendario": 1800}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "year" in str(exc_info.value).lower() or "1900" in str(exc_info.value)

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"anoCalendario": 2023}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "REGIMEAPURACAO"
        assert pedido_dados["idServico"] == "CONSULTAROPCAOREGIME103"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("REGIMEAPURACAO", "CONSULTAROPCAOREGIME103")
        assert template_class is not None
        assert template_class == ConsultarOpcaoRegime103Template


class TestConsultarResolucao104Template:
    """Tests for ConsultarResolucao104Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultarResolucao104Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "REGIMEAPURACAO"
        assert template.id_servico == "CONSULTARRESOLUCAO104"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid anoCalendario."""
        dados = {"anoCalendario": 2021}
        result = template.validate(dados)
        assert result["anoCalendario"] == 2021

    def test_validate_ano_as_string(self, template):
        """Test validation accepts anoCalendario as string and converts to int."""
        dados = {"anoCalendario": "2021"}
        result = template.validate(dados)
        assert result["anoCalendario"] == 2021

    def test_validate_missing_ano(self, template):
        """Test validation fails when anoCalendario is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_year_range(self, template):
        """Test validation fails with year out of range."""
        dados = {"anoCalendario": 1800}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "year" in str(exc_info.value).lower() or "1900" in str(exc_info.value)

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"anoCalendario": 2021}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "REGIMEAPURACAO"
        assert pedido_dados["idServico"] == "CONSULTARRESOLUCAO104"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("REGIMEAPURACAO", "CONSULTARRESOLUCAO104")
        assert template_class is not None
        assert template_class == ConsultarResolucao104Template


