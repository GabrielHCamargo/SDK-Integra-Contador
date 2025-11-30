"""Unit tests for EVENTOS ATUALIZACAO templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.eventosatualizacao.monitorar import (
    SoliEventosPf131Template,
    ObterEventosPf133Template,
    SoliEventosPj132Template,
    ObterEventosPj134Template,
)
from integra_sdk.templates.registry import TemplateRegistry


class TestSoliEventosPf131Template:
    """Tests for SoliEventosPf131Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return SoliEventosPf131Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "EVENTOSATUALIZACAO"
        assert template.id_servico == "SOLICEVENTOSPF131"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Monitorar"

    def test_validate_success(self, template):
        """Test successful validation with valid evento."""
        dados = {"evento": "E0301"}
        result = template.validate(dados)
        assert result["evento"] == "E0301"

    def test_validate_success_with_whitespace(self, template):
        """Test successful validation with evento containing whitespace."""
        dados = {"evento": "  E0301  "}
        result = template.validate(dados)
        assert result["evento"] == "E0301"

    def test_validate_missing_evento(self, template):
        """Test validation fails when evento is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "evento" in str(exc_info.value).lower()

    def test_validate_invalid_evento_type(self, template):
        """Test validation fails when evento has invalid type."""
        dados = {"evento": 123}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "evento" in str(exc_info.value).lower()

    def test_validate_empty_evento(self, template):
        """Test validation fails when evento is empty."""
        dados = {"evento": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "evento" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000", "tipo": 3}

        dados = {"evento": "E0301"}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "EVENTOSATUALIZACAO"
        assert pedido_dados["idServico"] == "SOLICEVENTOSPF131"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert "dados" in pedido_dados

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("EVENTOSATUALIZACAO", "SOLICEVENTOSPF131")
        assert template_class is not None
        assert template_class == SoliEventosPf131Template


class TestObterEventosPf133Template:
    """Tests for ObterEventosPf133Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ObterEventosPf133Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "EVENTOSATUALIZACAO"
        assert template.id_servico == "OBTEREVENTOSPF133"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Monitorar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"protocolo": "a65f3455-fa91-419b-b0ad-c4ac50695abf", "evento": "E0301"}
        result = template.validate(dados)
        assert result["protocolo"] == "a65f3455-fa91-419b-b0ad-c4ac50695abf"
        assert result["evento"] == "E0301"

    def test_validate_missing_protocolo(self, template):
        """Test validation fails when protocolo is missing."""
        dados = {"evento": "E0301"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "protocolo" in str(exc_info.value).lower()

    def test_validate_missing_evento(self, template):
        """Test validation fails when evento is missing."""
        dados = {"protocolo": "a65f3455-fa91-419b-b0ad-c4ac50695abf"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "evento" in str(exc_info.value).lower()

    def test_validate_empty_protocolo(self, template):
        """Test validation fails when protocolo is empty."""
        dados = {"protocolo": "", "evento": "E0301"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "protocolo" in str(exc_info.value).lower()

    def test_validate_empty_evento(self, template):
        """Test validation fails when evento is empty."""
        dados = {"protocolo": "a65f3455-fa91-419b-b0ad-c4ac50695abf", "evento": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "evento" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "", "tipo": 3}

        dados = {"protocolo": "a65f3455-fa91-419b-b0ad-c4ac50695abf", "evento": "E0301"}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "EVENTOSATUALIZACAO"
        assert pedido_dados["idServico"] == "OBTEREVENTOSPF133"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert "dados" in pedido_dados

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("EVENTOSATUALIZACAO", "OBTEREVENTOSPF133")
        assert template_class is not None
        assert template_class == ObterEventosPf133Template


class TestSoliEventosPj132Template:
    """Tests for SoliEventosPj132Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return SoliEventosPj132Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "EVENTOSATUALIZACAO"
        assert template.id_servico == "SOLICEVENTOSPJ132"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Monitorar"

    def test_validate_success(self, template):
        """Test successful validation with valid evento."""
        dados = {"evento": "E0301"}
        result = template.validate(dados)
        assert result["evento"] == "E0301"

    def test_validate_missing_evento(self, template):
        """Test validation fails when evento is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "evento" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 4}

        dados = {"evento": "E0301"}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "EVENTOSATUALIZACAO"
        assert pedido_dados["idServico"] == "SOLICEVENTOSPJ132"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert "dados" in pedido_dados

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("EVENTOSATUALIZACAO", "SOLICEVENTOSPJ132")
        assert template_class is not None
        assert template_class == SoliEventosPj132Template


class TestObterEventosPj134Template:
    """Tests for ObterEventosPj134Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ObterEventosPj134Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "EVENTOSATUALIZACAO"
        assert template.id_servico == "OBTEREVENTOSPJ134"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Monitorar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"protocolo": "q90n3455-fa91-419c-c0ad-a4ms50215acl", "evento": "E0301"}
        result = template.validate(dados)
        assert result["protocolo"] == "q90n3455-fa91-419c-c0ad-a4ms50215acl"
        assert result["evento"] == "E0301"

    def test_validate_missing_protocolo(self, template):
        """Test validation fails when protocolo is missing."""
        dados = {"evento": "E0301"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "protocolo" in str(exc_info.value).lower()

    def test_validate_missing_evento(self, template):
        """Test validation fails when evento is missing."""
        dados = {"protocolo": "q90n3455-fa91-419c-c0ad-a4ms50215acl"}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "evento" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "", "tipo": 4}

        dados = {"protocolo": "q90n3455-fa91-419c-c0ad-a4ms50215acl", "evento": "E0301"}
        request = template.build_request(config, dados)

        assert "contratante" in request
        assert "autorPedidoDados" in request
        assert "contribuinte" in request
        assert "pedidoDados" in request

        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "EVENTOSATUALIZACAO"
        assert pedido_dados["idServico"] == "OBTEREVENTOSPJ134"
        assert pedido_dados["versaoSistema"] == "1.0"
        assert "dados" in pedido_dados

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("EVENTOSATUALIZACAO", "OBTEREVENTOSPJ134")
        assert template_class is not None
        assert template_class == ObterEventosPj134Template

