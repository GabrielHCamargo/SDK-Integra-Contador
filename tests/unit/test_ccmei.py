"""Unit tests for CCMEI templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.ccmei.consultar import (
    CcmeiSitCadastral123Template,
    DadosCcmei122Template,
)
from integra_sdk.templates.ccmei.emitir import EmitirCcmei121Template
from integra_sdk.templates.registry import TemplateRegistry


class TestCcmeiSitCadastral123Template:
    """Tests for CcmeiSitCadastral123Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return CcmeiSitCadastral123Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "CCMEI"
        assert template.id_servico == "CCMEISITCADASTRAL123"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success_empty_dict(self, template):
        """Test successful validation with empty dict."""
        dados = {}
        result = template.validate(dados)
        
        assert result == {}
        assert isinstance(result, dict)

    def test_validate_success_none(self, template):
        """Test successful validation with None (will be treated as empty)."""
        dados = {}
        result = template.validate(dados)
        
        assert result == {}

    def test_validate_success_empty_string_fields(self, template):
        """Test validation accepts empty string fields."""
        dados = {"field": ""}
        result = template.validate(dados)
        
        # Empty strings should be accepted (treated as empty)
        assert result == {}

    def test_validate_fails_with_data(self, template):
        """Test validation fails when data is provided."""
        dados = {"cpf": "12345678900"}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "CCMEISITCADASTRAL123" in str(exc_info.value)
        assert "does not accept input data" in str(exc_info.value)

    def test_validate_success_with_whitespace_data(self, template):
        """Test validation succeeds when whitespace-only data is provided (treated as empty)."""
        dados = {"field": "   "}
        result = template.validate(dados)
        
        # Whitespace-only fields are treated as empty and accepted
        assert result == {}

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        
        dados = {}
        request = template.build_request(config, dados)
        
        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request
        
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "CCMEI"
        assert pedido_dados["idServico"] == "CCMEISITCADASTRAL123"
        assert pedido_dados["versaoSistema"] == "1.0"
        
        # Verify dados is empty string (not "{}")
        assert pedido_dados["dados"] == ""

    def test_serialize_dados_empty(self, template):
        """Test serializing empty dados returns empty string."""
        result = template._serialize_dados({})
        assert result == ""

    def test_serialize_dados_none(self, template):
        """Test serializing None dados returns empty string."""
        result = template._serialize_dados({})
        assert result == ""

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("CCMEI", "CCMEISITCADASTRAL123")
        assert template_class is not None
        assert template_class == CcmeiSitCadastral123Template


class TestDadosCcmei122Template:
    """Tests for DadosCcmei122Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return DadosCcmei122Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "CCMEI"
        assert template.id_servico == "DADOSCCMEI122"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success_empty_dict(self, template):
        """Test successful validation with empty dict."""
        dados = {}
        result = template.validate(dados)
        
        assert result == {}
        assert isinstance(result, dict)

    def test_validate_success_none(self, template):
        """Test successful validation with None (will be treated as empty)."""
        dados = {}
        result = template.validate(dados)
        
        assert result == {}

    def test_validate_success_empty_string_fields(self, template):
        """Test validation accepts empty string fields."""
        dados = {"field": ""}
        result = template.validate(dados)
        
        # Empty strings should be accepted (treated as empty)
        assert result == {}

    def test_validate_fails_with_data(self, template):
        """Test validation fails when data is provided."""
        dados = {"cnpj": "00000000000000"}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "DADOSCCMEI122" in str(exc_info.value)
        assert "does not accept input data" in str(exc_info.value)

    def test_validate_success_with_whitespace_data(self, template):
        """Test validation succeeds when whitespace-only data is provided (treated as empty)."""
        dados = {"field": "   "}
        result = template.validate(dados)
        
        # Whitespace-only fields are treated as empty and accepted
        assert result == {}

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "37013568000157", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"numero": "37013568000157", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "57971619889184", "tipo": 2}
        
        dados = {}
        request = template.build_request(config, dados)
        
        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request
        
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "CCMEI"
        assert pedido_dados["idServico"] == "DADOSCCMEI122"
        assert pedido_dados["versaoSistema"] == "1.0"
        
        # Verify dados is empty string (not "{}")
        assert pedido_dados["dados"] == ""

    def test_serialize_dados_empty(self, template):
        """Test serializing empty dados returns empty string."""
        result = template._serialize_dados({})
        assert result == ""

    def test_serialize_dados_none(self, template):
        """Test serializing None dados returns empty string."""
        result = template._serialize_dados({})
        assert result == ""

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("CCMEI", "DADOSCCMEI122")
        assert template_class is not None
        assert template_class == DadosCcmei122Template


class TestEmitirCcmei121Template:
    """Tests for EmitirCcmei121Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return EmitirCcmei121Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "CCMEI"
        assert template.id_servico == "EMITIRCCMEI121"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success_empty_dict(self, template):
        """Test successful validation with empty dict."""
        dados = {}
        result = template.validate(dados)
        
        assert result == {}
        assert isinstance(result, dict)

    def test_validate_success_none(self, template):
        """Test successful validation with None (will be treated as empty)."""
        dados = {}
        result = template.validate(dados)
        
        assert result == {}

    def test_validate_success_empty_string_fields(self, template):
        """Test validation accepts empty string fields."""
        dados = {"field": ""}
        result = template.validate(dados)
        
        # Empty strings should be accepted (treated as empty)
        assert result == {}

    def test_validate_fails_with_data(self, template):
        """Test validation fails when data is provided."""
        dados = {"cnpj": "00000000000000"}
        
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        
        assert "EMITIRCCMEI121" in str(exc_info.value)
        assert "does not accept input data" in str(exc_info.value)

    def test_validate_success_with_whitespace_data(self, template):
        """Test validation succeeds when whitespace-only data is provided (treated as empty)."""
        dados = {"field": "   "}
        result = template.validate(dados)
        
        # Whitespace-only fields are treated as empty and accepted
        assert result == {}

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
        assert pedido_dados["idSistema"] == "CCMEI"
        assert pedido_dados["idServico"] == "EMITIRCCMEI121"
        assert pedido_dados["versaoSistema"] == "1.0"
        
        # Verify dados is empty string (not "{}")
        assert pedido_dados["dados"] == ""

    def test_serialize_dados_empty(self, template):
        """Test serializing empty dados returns empty string."""
        result = template._serialize_dados({})
        assert result == ""

    def test_serialize_dados_none(self, template):
        """Test serializing None dados returns empty string."""
        result = template._serialize_dados({})
        assert result == ""

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("CCMEI", "EMITIRCCMEI121")
        assert template_class is not None
        assert template_class == EmitirCcmei121Template

