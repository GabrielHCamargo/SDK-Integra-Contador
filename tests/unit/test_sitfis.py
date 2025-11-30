"""Unit tests for SITFIS templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.sitfis.apoiar import SolicitarProtocolo91Template
from integra_sdk.templates.sitfis.emitir import RelatorioSitfis92Template
from integra_sdk.templates.registry import TemplateRegistry


class TestSolicitarProtocolo91Template:
    """Tests for SolicitarProtocolo91Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return SolicitarProtocolo91Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "SITFIS"
        assert template.id_servico == "SOLICITARPROTOCOLO91"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Apoiar"

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
        config.contribuinte.model_dump.return_value = {"numero": "99999999999", "tipo": 1}

        dados = {}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "SITFIS"
        assert pedido_dados["idServico"] == "SOLICITARPROTOCOLO91"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("SITFIS", "SOLICITARPROTOCOLO91")
        assert template_class is not None
        assert template_class == SolicitarProtocolo91Template


class TestRelatorioSitfis92Template:
    """Tests for RelatorioSitfis92Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return RelatorioSitfis92Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "SITFIS"
        assert template.id_servico == "RELATORIOSITFIS92"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid protocoloRelatorio."""
        dados = {
            "protocoloRelatorio": "+S7N6c04XNZUVzmxWT7SzpkZA4xeDQC9Z2T2GBJ5usn8LyouyWXbsy6mKsLy7/EImRkDjF4NAL25KiSXOLjnzAaZu/FC+G1pYOtTMYqokKYYr/yZ6aqUiCuWPfujDQ2/udwgU+Dyh56GSe28B5Ev25jDnzpvVJPhiebO5hpy1YESP5gnEhaP3bocCiZZrYG26F8avRRBJhRTsfv3Rvop+bxvYJZsVym270eO8oZTDIr3OJj=="
        }
        result = template.validate(dados)
        assert result["protocoloRelatorio"] == dados["protocoloRelatorio"]

    def test_validate_missing_protocolo(self, template):
        """Test validation fails when protocoloRelatorio is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "protocolo" in str(exc_info.value).lower()

    def test_validate_empty_protocolo(self, template):
        """Test validation fails when protocoloRelatorio is empty."""
        dados = {"protocoloRelatorio": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_invalid_protocolo_type(self, template):
        """Test validation fails when protocoloRelatorio is not a string."""
        dados = {"protocoloRelatorio": 12345}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "string" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999", "tipo": 1}

        dados = {
            "protocoloRelatorio": "+S7N6c04XNZUVzmxWT7SzpkZA4xeDQC9Z2T2GBJ5usn8LyouyWXbsy6mKsLy7/EImRkDjF4NAL25KiSXOLjnzAaZu/FC+G1pYOtTMYqokKYYr/yZ6aqUiCuWPfujDQ2/udwgU+Dyh56GSe28B5Ev25jDnzpvVJPhiebO5hpy1YESP5gnEhaP3bocCiZZrYG26F8avRRBJhRTsfv3Rvop+bxvYJZsVym270eO8oZTDIr3OJj=="
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "SITFIS"
        assert pedido_dados["idServico"] == "RELATORIOSITFIS92"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("SITFIS", "RELATORIOSITFIS92")
        assert template_class is not None
        assert template_class == RelatorioSitfis92Template


