"""Unit tests for PERTSN templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.pertsn.consultar import (
    PedidosParc183Template,
    ObterParc184Template,
    ParcelasParaGerar182Template,
    DetPagtoParc185Template,
)
from integra_sdk.templates.pertsn.emitir import Gerardas181Template
from integra_sdk.templates.registry import TemplateRegistry


class TestPedidosParc183Template:
    """Tests for PedidosParc183Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return PedidosParc183Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTSN"
        assert template.id_servico == "PEDIDOSPARC183"
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
        assert pedido_dados["idSistema"] == "PERTSN"
        assert pedido_dados["idServico"] == "PEDIDOSPARC183"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTSN", "PEDIDOSPARC183")
        assert template_class is not None
        assert template_class == PedidosParc183Template


class TestObterParc184Template:
    """Tests for ObterParc184Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ObterParc184Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTSN"
        assert template.id_servico == "OBTERPARC184"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid numeroParcelamento."""
        dados = {"numeroParcelamento": 9102}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9102

    def test_validate_numero_as_string(self, template):
        """Test validation accepts numeroParcelamento as string."""
        dados = {"numeroParcelamento": "9102"}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9102

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroParcelamento is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_negative_numero(self, template):
        """Test validation fails when numeroParcelamento is negative."""
        dados = {"numeroParcelamento": -1}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "non-negative" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroParcelamento": 9102}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PERTSN"
        assert pedido_dados["idServico"] == "OBTERPARC184"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTSN", "OBTERPARC184")
        assert template_class is not None
        assert template_class == ObterParc184Template


class TestParcelasParaGerar182Template:
    """Tests for ParcelasParaGerar182Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ParcelasParaGerar182Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTSN"
        assert template.id_servico == "PARCELASPARAGERAR182"
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
        assert pedido_dados["idSistema"] == "PERTSN"
        assert pedido_dados["idServico"] == "PARCELASPARAGERAR182"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTSN", "PARCELASPARAGERAR182")
        assert template_class is not None
        assert template_class == ParcelasParaGerar182Template


class TestDetPagtoParc185Template:
    """Tests for DetPagtoParc185Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return DetPagtoParc185Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTSN"
        assert template.id_servico == "DETPAGTOPARC185"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"numeroParcelamento": 9102, "anoMesParcela": 201806}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9102
        assert result["anoMesParcela"] == 201806

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroParcelamento is missing."""
        dados = {"anoMesParcela": 201806}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_missing_ano_mes(self, template):
        """Test validation fails when anoMesParcela is missing."""
        dados = {"numeroParcelamento": 9102}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_ano_mes_format(self, template):
        """Test validation fails with invalid anoMesParcela format."""
        dados = {"numeroParcelamento": 9102, "anoMesParcela": 180000}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_validate_string_values(self, template):
        """Test validation accepts string values and converts them."""
        dados = {"numeroParcelamento": "9102", "anoMesParcela": "201806"}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9102
        assert result["anoMesParcela"] == 201806

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroParcelamento": 9102, "anoMesParcela": 201806}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PERTSN"
        assert pedido_dados["idServico"] == "DETPAGTOPARC185"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTSN", "DETPAGTOPARC185")
        assert template_class is not None
        assert template_class == DetPagtoParc185Template


class TestGerardas181Template:
    """Tests for Gerardas181Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Gerardas181Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTSN"
        assert template.id_servico == "GERARDAS181"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid parcelaParaEmitir."""
        dados = {"parcelaParaEmitir": 202301}
        result = template.validate(dados)
        assert result["parcelaParaEmitir"] == 202301

    def test_validate_parcela_as_string(self, template):
        """Test validation accepts parcelaParaEmitir as string."""
        dados = {"parcelaParaEmitir": "202301"}
        result = template.validate(dados)
        assert result["parcelaParaEmitir"] == 202301

    def test_validate_missing_parcela(self, template):
        """Test validation fails when parcelaParaEmitir is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "parcela" in str(exc_info.value).lower()

    def test_validate_invalid_parcela_format(self, template):
        """Test validation fails with invalid parcelaParaEmitir format."""
        dados = {"parcelaParaEmitir": 180000}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"parcelaParaEmitir": 202301}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PERTSN"
        assert pedido_dados["idServico"] == "GERARDAS181"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTSN", "GERARDAS181")
        assert template_class is not None
        assert template_class == Gerardas181Template

