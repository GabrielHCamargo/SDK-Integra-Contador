"""Unit tests for PROCURACOES templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.procuracoes.consultar import ObterProcuracao41Template
from integra_sdk.templates.registry import TemplateRegistry


class TestObterProcuracao41Template:
    """Tests for ObterProcuracao41Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ObterProcuracao41Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PROCURACOES"
        assert template.id_servico == "OBTERPROCURACAO41"
        assert template.versao_sistema == "1"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {
            "outorgante": "99999999999999",
            "tipoOutorgante": "2",
            "outorgado": "99999999999",
            "tipoOutorgado": "1",
        }
        result = template.validate(dados)
        assert result["outorgante"] == "99999999999999"
        assert result["tipoOutorgante"] == "2"
        assert result["outorgado"] == "99999999999"
        assert result["tipoOutorgado"] == "1"

    def test_validate_numeric_values(self, template):
        """Test validation accepts numeric values and converts to string."""
        dados = {
            "outorgante": 99999999999999,
            "tipoOutorgante": 2,
            "outorgado": 99999999999,
            "tipoOutorgado": 1,
        }
        result = template.validate(dados)
        assert result["outorgante"] == "99999999999999"
        assert result["tipoOutorgante"] == "2"
        assert result["outorgado"] == "99999999999"
        assert result["tipoOutorgado"] == "1"

    def test_validate_missing_outorgante(self, template):
        """Test validation fails when outorgante is missing."""
        dados = {
            "tipoOutorgante": "2",
            "outorgado": "99999999999",
            "tipoOutorgado": "1",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "outorgante" in str(exc_info.value).lower()

    def test_validate_missing_tipo_outorgante(self, template):
        """Test validation fails when tipoOutorgante is missing."""
        dados = {
            "outorgante": "99999999999999",
            "outorgado": "99999999999",
            "tipoOutorgado": "1",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "tipo" in str(exc_info.value).lower()

    def test_validate_missing_outorgado(self, template):
        """Test validation fails when outorgado is missing."""
        dados = {
            "outorgante": "99999999999999",
            "tipoOutorgante": "2",
            "tipoOutorgado": "1",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "outorgado" in str(exc_info.value).lower()

    def test_validate_missing_tipo_outorgado(self, template):
        """Test validation fails when tipoOutorgado is missing."""
        dados = {
            "outorgante": "99999999999999",
            "tipoOutorgante": "2",
            "outorgado": "99999999999",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "tipo" in str(exc_info.value).lower()

    def test_validate_invalid_tipo_outorgante(self, template):
        """Test validation fails with invalid tipoOutorgante."""
        dados = {
            "outorgante": "99999999999999",
            "tipoOutorgante": "3",
            "outorgado": "99999999999",
            "tipoOutorgado": "1",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "tipoOutorgante" in str(exc_info.value) or "1" in str(exc_info.value) or "2" in str(exc_info.value)

    def test_validate_invalid_tipo_outorgado(self, template):
        """Test validation fails with invalid tipoOutorgado."""
        dados = {
            "outorgante": "99999999999999",
            "tipoOutorgante": "2",
            "outorgado": "99999999999",
            "tipoOutorgado": "3",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "tipoOutorgado" in str(exc_info.value) or "1" in str(exc_info.value) or "2" in str(exc_info.value)

    def test_validate_empty_outorgante(self, template):
        """Test validation fails when outorgante is empty."""
        dados = {
            "outorgante": "",
            "tipoOutorgante": "2",
            "outorgado": "99999999999",
            "tipoOutorgado": "1",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_empty_outorgado(self, template):
        """Test validation fails when outorgado is empty."""
        dados = {
            "outorgante": "99999999999999",
            "tipoOutorgante": "2",
            "outorgado": "",
            "tipoOutorgado": "1",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999", "tipo": 1}

        dados = {
            "outorgante": "99999999999999",
            "tipoOutorgante": "2",
            "outorgado": "99999999999",
            "tipoOutorgado": "1",
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PROCURACOES"
        assert pedido_dados["idServico"] == "OBTERPROCURACAO41"
        assert pedido_dados["versaoSistema"] == "1"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PROCURACOES", "OBTERPROCURACAO41")
        assert template_class is not None
        assert template_class == ObterProcuracao41Template


