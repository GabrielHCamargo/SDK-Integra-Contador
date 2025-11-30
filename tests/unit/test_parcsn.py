"""Unit tests for PARCSN templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.parcsn.consultar import (
    PedidosParc163Template,
    ObterParc164Template,
    ParcelasParaGerar162Template,
    DetPagtoParc165Template,
)
from integra_sdk.templates.parcsn.emitir import Gerardas161Template
from integra_sdk.templates.registry import TemplateRegistry


class TestPedidosParc163Template:
    """Tests for PedidosParc163Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return PedidosParc163Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCSN"
        assert template.id_servico == "PEDIDOSPARC163"
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
        assert pedido_dados["idSistema"] == "PARCSN"
        assert pedido_dados["idServico"] == "PEDIDOSPARC163"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCSN", "PEDIDOSPARC163")
        assert template_class is not None
        assert template_class == PedidosParc163Template


class TestObterParc164Template:
    """Tests for ObterParc164Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ObterParc164Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCSN"
        assert template.id_servico == "OBTERPARC164"
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
        assert pedido_dados["idSistema"] == "PARCSN"
        assert pedido_dados["idServico"] == "OBTERPARC164"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCSN", "OBTERPARC164")
        assert template_class is not None
        assert template_class == ObterParc164Template


class TestParcelasParaGerar162Template:
    """Tests for ParcelasParaGerar162Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ParcelasParaGerar162Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCSN"
        assert template.id_servico == "PARCELASPARAGERAR162"
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
        assert pedido_dados["idSistema"] == "PARCSN"
        assert pedido_dados["idServico"] == "PARCELASPARAGERAR162"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCSN", "PARCELASPARAGERAR162")
        assert template_class is not None
        assert template_class == ParcelasParaGerar162Template


class TestDetPagtoParc165Template:
    """Tests for DetPagtoParc165Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return DetPagtoParc165Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCSN"
        assert template.id_servico == "DETPAGTOPARC165"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"numeroParcelamento": 1, "anoMesParcela": 201612}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 1
        assert result["anoMesParcela"] == 201612

    def test_validate_missing_numero(self, template):
        """Test validation fails when numeroParcelamento is missing."""
        dados = {"anoMesParcela": 201612}
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
        dados = {"numeroParcelamento": "1", "anoMesParcela": "201612"}
        result = template.validate(dados)
        assert result["numeroParcelamento"] == 1
        assert result["anoMesParcela"] == 201612

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"numeroParcelamento": 1, "anoMesParcela": 201612}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "PARCSN"
        assert pedido_dados["idServico"] == "DETPAGTOPARC165"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCSN", "DETPAGTOPARC165")
        assert template_class is not None
        assert template_class == DetPagtoParc165Template


class TestGerardas161Template:
    """Tests for Gerardas161Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Gerardas161Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "PARCSN"
        assert template.id_servico == "GERARDAS161"
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
        assert pedido_dados["idSistema"] == "PARCSN"
        assert pedido_dados["idServico"] == "GERARDAS161"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("PARCSN", "GERARDAS161")
        assert template_class is not None
        assert template_class == Gerardas161Template

