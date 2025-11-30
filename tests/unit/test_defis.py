"""Unit tests for DEFIS templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.defis.declarar import TransDeclaracao141Template
from integra_sdk.templates.defis.consultar import (
    ConsDeclaracao142Template,
    ConsUltimaDecRec143Template,
    ConsDecRec144Template,
)
from integra_sdk.templates.registry import TemplateRegistry


class TestTransDeclaracao141Template:
    """Tests for TransDeclaracao141Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return TransDeclaracao141Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DEFIS"
        assert template.id_servico == "TRANSDECLARACAO141"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Declarar"

    def test_validate_success_minimal(self, template):
        """Test successful validation with minimal required fields."""
        dados = {
            "ano": 2021,
            "inatividade": 2,
        }
        result = template.validate(dados)

        assert result["ano"] == 2021
        assert result["inatividade"] == 2

    def test_validate_success_ano_string(self, template):
        """Test successful validation with ano as string."""
        dados = {
            "ano": "2021",
            "inatividade": 2,
        }
        result = template.validate(dados)

        assert result["ano"] == 2021

    def test_validate_success_inatividade_string(self, template):
        """Test successful validation with inatividade as string."""
        dados = {
            "ano": 2021,
            "inatividade": "2",
        }
        result = template.validate(dados)

        assert result["inatividade"] == 2

    def test_validate_success_with_optional_fields(self, template):
        """Test successful validation with optional fields."""
        dados = {
            "ano": 2021,
            "inatividade": 2,
            "situacaoEspecial": None,
            "empresa": {
                "ganhoCapital": 10.0,
                "qtdEmpregadoInicial": 20,
            },
            "naoOptante": None,
        }
        result = template.validate(dados)

        assert result["ano"] == 2021
        assert result["inatividade"] == 2
        assert result["situacaoEspecial"] is None
        assert "empresa" in result
        assert result["naoOptante"] is None

    def test_validate_missing_ano(self, template):
        """Test validation fails when ano is missing."""
        dados = {
            "inatividade": 2,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "ano" in str(exc_info.value).lower()

    def test_validate_missing_inatividade(self, template):
        """Test validation fails when inatividade is missing."""
        dados = {
            "ano": 2021,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "inatividade" in str(exc_info.value).lower()

    def test_validate_invalid_ano_type(self, template):
        """Test validation fails when ano has invalid type."""
        dados = {
            "ano": [2021],  # Invalid type
            "inatividade": 2,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_ano_range(self, template):
        """Test validation fails when ano is out of valid range."""
        dados = {
            "ano": 1800,  # Too old
            "inatividade": 2,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_inatividade_type(self, template):
        """Test validation fails when inatividade has invalid type."""
        dados = {
            "ano": 2021,
            "inatividade": [2],  # Invalid type
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "inatividade" in str(exc_info.value).lower()

    def test_validate_invalid_inatividade_negative(self, template):
        """Test validation fails when inatividade is negative."""
        dados = {
            "ano": 2021,
            "inatividade": -1,
        }

        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)

        assert "inatividade" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "ano": 2021,
            "inatividade": 2,
        }
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DEFIS"
        assert pedido_dados["idServico"] == "TRANSDECLARACAO141"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert "dados" in pedido_dados

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DEFIS", "TRANSDECLARACAO141")
        assert template_class is not None
        assert template_class == TransDeclaracao141Template


class TestConsDeclaracao142Template:
    """Tests for ConsDeclaracao142Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsDeclaracao142Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DEFIS"
        assert template.id_servico == "CONSDECLARACAO142"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success_empty(self, template):
        """Test successful validation with empty dados."""
        dados = {}
        result = template.validate(dados)
        assert result == {}

    def test_validate_fails_with_data(self, template):
        """Test validation fails when dados contains data."""
        dados = {"ano": 2021}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "does not accept input data" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DEFIS"
        assert pedido_dados["idServico"] == "CONSDECLARACAO142"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert pedido_dados["dados"] == ""

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DEFIS", "CONSDECLARACAO142")
        assert template_class is not None
        assert template_class == ConsDeclaracao142Template


class TestConsUltimaDecRec143Template:
    """Tests for ConsUltimaDecRec143Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsUltimaDecRec143Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DEFIS"
        assert template.id_servico == "CONSULTIMADECREC143"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid ano."""
        dados = {"ano": 2021}
        result = template.validate(dados)
        assert result["ano"] == 2021

    def test_validate_success_ano_string(self, template):
        """Test successful validation with ano as string."""
        dados = {"ano": "2021"}
        result = template.validate(dados)
        assert result["ano"] == 2021

    def test_validate_missing_ano(self, template):
        """Test validation fails when ano is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_ano_type(self, template):
        """Test validation fails when ano has invalid type."""
        dados = {"ano": [2021]}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_ano_range(self, template):
        """Test validation fails when ano is out of valid range."""
        dados = {"ano": 1800}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"ano": 2021}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DEFIS"
        assert pedido_dados["idServico"] == "CONSULTIMADECREC143"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert "dados" in pedido_dados

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DEFIS", "CONSULTIMADECREC143")
        assert template_class is not None
        assert template_class == ConsUltimaDecRec143Template


class TestConsDecRec144Template:
    """Tests for ConsDecRec144Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsDecRec144Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DEFIS"
        assert template.id_servico == "CONSDECREC144"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid idDefis."""
        dados = {"idDefis": "000000002021002"}
        result = template.validate(dados)
        assert result["idDefis"] == "000000002021002"

    def test_validate_success_with_whitespace(self, template):
        """Test successful validation with idDefis containing whitespace."""
        dados = {"idDefis": "  000000002021002  "}
        result = template.validate(dados)
        assert result["idDefis"] == "000000002021002"

    def test_validate_missing_id_defis(self, template):
        """Test validation fails when idDefis is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "iddefis" in str(exc_info.value).lower()

    def test_validate_invalid_id_defis_type(self, template):
        """Test validation fails when idDefis has invalid type."""
        dados = {"idDefis": 123}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "iddefis" in str(exc_info.value).lower()

    def test_validate_empty_id_defis(self, template):
        """Test validation fails when idDefis is empty."""
        dados = {"idDefis": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "iddefis" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"idDefis": "000000002021002"}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DEFIS"
        assert pedido_dados["idServico"] == "CONSDECREC144"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert "dados" in pedido_dados

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DEFIS", "CONSDECREC144")
        assert template_class is not None
        assert template_class == ConsDecRec144Template

