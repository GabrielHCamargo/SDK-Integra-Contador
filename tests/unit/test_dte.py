"""Unit tests for DTE templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.dte.consultar import ConsultaSituacaoDte111Template
from integra_sdk.templates.registry import TemplateRegistry


class TestConsultaSituacaoDte111Template:
    """Tests for ConsultaSituacaoDte111Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultaSituacaoDte111Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "DTE"
        assert template.id_servico == "CONSULTASITUACAODTE111"
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
        config.contratante.model_dump.return_value = {"numero": "11111111111111", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "11111111111111", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}

        dados = {}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "DTE"
        assert pedido_dados["idServico"] == "CONSULTASITUACAODTE111"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert pedido_dados["dados"] == ""

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("DTE", "CONSULTASITUACAODTE111")
        assert template_class is not None
        assert template_class == ConsultaSituacaoDte111Template

