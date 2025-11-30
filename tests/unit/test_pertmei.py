"""Unit tests for PERTMEI templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.pertmei.consultar import (
    PedidosParc223Template,
    ObterParc224Template,
    ParcelasParaGerar222Template,
    DetPagtoParc225Template,
)
from integra_sdk.templates.pertmei.emitir import Gerardas221Template
from integra_sdk.templates.registry import TemplateRegistry


class TestPedidosParc223Template:
    """Tests for PedidosParc223Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return PedidosParc223Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTMEI"
        assert template.id_servico == "PEDIDOSPARC223"
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
        assert pedido_dados["idSistema"] == "PERTMEI"
        assert pedido_dados["idServico"] == "PEDIDOSPARC223"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTMEI", "PEDIDOSPARC223")
        assert template_class is not None
        assert template_class == PedidosParc223Template


class TestObterParc224Template:
    """Tests for ObterParc224Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ObterParc224Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTMEI"
        assert template.id_servico == "OBTERPARC224"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid numeroParcelamento."""
        dados = {"numeroParcelamento": 9001}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9001

    def test_validate_numero_as_string(self, template):
        """Test validation accepts numeroParcelamento as string."""
        dados = {"numeroParcelamento": "9001"}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9001

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

        dados = {"numeroParcelamento": 9001}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PERTMEI"
        assert pedido_dados["idServico"] == "OBTERPARC224"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTMEI", "OBTERPARC224")
        assert template_class is not None
        assert template_class == ObterParc224Template


class TestParcelasParaGerar222Template:
    """Tests for ParcelasParaGerar222Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ParcelasParaGerar222Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTMEI"
        assert template.id_servico == "PARCELASPARAGERAR222"
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
        assert pedido_dados["idSistema"] == "PERTMEI"
        assert pedido_dados["idServico"] == "PARCELASPARAGERAR222"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTMEI", "PARCELASPARAGERAR222")
        assert template_class is not None
        assert template_class == ParcelasParaGerar222Template


class TestDetPagtoParc225Template:
    """Tests for DetPagtoParc225Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return DetPagtoParc225Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTMEI"
        assert template.id_servico == "DETPAGTOPARC225"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"numeroParcelamento": 9101, "anoMesParcela": 201907}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9101
        assert result["anoMesParcela"] == 201907

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroParcelamento is missing."""
        dados = {"anoMesParcela": 201907}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_missing_ano_mes(self, template):
        """Test validation fails when anoMesParcela is missing."""
        dados = {"numeroParcelamento": 9101}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_ano_mes_format(self, template):
        """Test validation fails with invalid anoMesParcela format."""
        dados = {"numeroParcelamento": 9101, "anoMesParcela": 180000}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_validate_string_values(self, template):
        """Test validation accepts string values and converts them."""
        dados = {"numeroParcelamento": "9101", "anoMesParcela": "201907"}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 9101
        assert result["anoMesParcela"] == 201907

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroParcelamento": 9101, "anoMesParcela": 201907}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PERTMEI"
        assert pedido_dados["idServico"] == "DETPAGTOPARC225"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTMEI", "DETPAGTOPARC225")
        assert template_class is not None
        assert template_class == DetPagtoParc225Template


class TestGerardas221Template:
    """Tests for Gerardas221Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Gerardas221Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PERTMEI"
        assert template.id_servico == "GERARDAS221"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid parcelaParaEmitir."""
        dados = {"parcelaParaEmitir": 202306}
        result = template.validate(dados)
        assert result["parcelaParaEmitir"] == 202306

    def test_validate_parcela_as_string(self, template):
        """Test validation accepts parcelaParaEmitir as string."""
        dados = {"parcelaParaEmitir": "202306"}
        result = template.validate(dados)
        assert result["parcelaParaEmitir"] == 202306

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

        dados = {"parcelaParaEmitir": 202306}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PERTMEI"
        assert pedido_dados["idServico"] == "GERARDAS221"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PERTMEI", "GERARDAS221")
        assert template_class is not None
        assert template_class == Gerardas221Template

