"""Unit tests for PARCMEI templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.parcmei.consultar import (
    PedidosParc203Template,
    ObterParc204Template,
    ParcelasParaGerar202Template,
    DetPagtoParc205Template,
)
from integra_sdk.templates.parcmei.emitir import Gerardas201Template
from integra_sdk.templates.registry import TemplateRegistry


class TestPedidosParc203Template:
    """Tests for PedidosParc203Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return PedidosParc203Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCMEI"
        assert template.id_servico == "PEDIDOSPARC203"
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
        assert pedido_dados["idSistema"] == "PARCMEI"
        assert pedido_dados["idServico"] == "PEDIDOSPARC203"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCMEI", "PEDIDOSPARC203")
        assert template_class is not None
        assert template_class == PedidosParc203Template


class TestObterParc204Template:
    """Tests for ObterParc204Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ObterParc204Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCMEI"
        assert template.id_servico == "OBTERPARC204"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid numeroParcelamento."""
        dados = {"numeroParcelamento": 1}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 1

    def test_validate_numero_as_string(self, template):
        """Test validation accepts numeroParcelamento as string."""
        dados = {"numeroParcelamento": "1"}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 1

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

        dados = {"numeroParcelamento": 1}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PARCMEI"
        assert pedido_dados["idServico"] == "OBTERPARC204"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCMEI", "OBTERPARC204")
        assert template_class is not None
        assert template_class == ObterParc204Template


class TestParcelasParaGerar202Template:
    """Tests for ParcelasParaGerar202Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ParcelasParaGerar202Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCMEI"
        assert template.id_servico == "PARCELASPARAGERAR202"
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
        assert pedido_dados["idSistema"] == "PARCMEI"
        assert pedido_dados["idServico"] == "PARCELASPARAGERAR202"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCMEI", "PARCELASPARAGERAR202")
        assert template_class is not None
        assert template_class == ParcelasParaGerar202Template


class TestDetPagtoParc205Template:
    """Tests for DetPagtoParc205Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return DetPagtoParc205Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCMEI"
        assert template.id_servico == "DETPAGTOPARC205"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"numeroParcelamento": 1, "anoMesParcela": 202107}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 1
        assert result["anoMesParcela"] == 202107

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroParcelamento is missing."""
        dados = {"anoMesParcela": 202107}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "numero" in str(exc_info.value).lower()

    def test_validate_missing_ano_mes(self, template):
        """Test validation fails when anoMesParcela is missing."""
        dados = {"numeroParcelamento": 1}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_invalid_ano_mes_format(self, template):
        """Test validation fails with invalid anoMesParcela format."""
        dados = {"numeroParcelamento": 1, "anoMesParcela": 180000}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "format" in str(exc_info.value).lower()

    def test_validate_string_values(self, template):
        """Test validation accepts string values and converts them."""
        dados = {"numeroParcelamento": "1", "anoMesParcela": "202107"}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 1
        assert result["anoMesParcela"] == 202107

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroParcelamento": 1, "anoMesParcela": 202107}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PARCMEI"
        assert pedido_dados["idServico"] == "DETPAGTOPARC205"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCMEI", "DETPAGTOPARC205")
        assert template_class is not None
        assert template_class == DetPagtoParc205Template


class TestGerardas201Template:
    """Tests for Gerardas201Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Gerardas201Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCMEI"
        assert template.id_servico == "GERARDAS201"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success(self, template):
        """Test successful validation with valid parcelaParaEmitir."""
        dados = {"parcelaParaEmitir": 202107}
        result = template.validate(dados)
        assert result["parcelaParaEmitir"] == 202107

    def test_validate_parcela_as_string(self, template):
        """Test validation accepts parcelaParaEmitir as string."""
        dados = {"parcelaParaEmitir": "202107"}
        result = template.validate(dados)
        assert result["parcelaParaEmitir"] == 202107

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

        dados = {"parcelaParaEmitir": 202107}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PARCMEI"
        assert pedido_dados["idServico"] == "GERARDAS201"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCMEI", "GERARDAS201")
        assert template_class is not None
        assert template_class == Gerardas201Template

