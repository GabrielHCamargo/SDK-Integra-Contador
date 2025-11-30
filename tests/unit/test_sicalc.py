"""Unit tests for SICALC templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.sicalc.emitir import (
    ConsolidarGerarDarf51Template,
    GerarDarfCodBarra53Template,
)
from integra_sdk.templates.sicalc.apoiar import ConsultaApoioReceitas52Template
from integra_sdk.templates.registry import TemplateRegistry


class TestConsolidarGerarDarf51Template:
    """Tests for ConsolidarGerarDarf51Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsolidarGerarDarf51Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "SICALC"
        assert template.id_servico == "CONSOLIDARGERARDARF51"
        assert template.versao_sistema == "2.9"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success_pessoa_fisica(self, template):
        """Test successful validation for Pessoa Física DARF."""
        dados = {
            "uf": "SP",
            "municipio": "7107",
            "codigoReceita": "0190",
            "codigoReceitaExtensao": "01",
            "tipoPA": "ME",
            "dataPA": "12/2017",
            "vencimento": "2018-01-31T00:00:00",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2022-08-08T00:00:00",
            "observacao": "Darf calculado",
        }
        result = template.validate(dados)
        assert result == dados

    def test_validate_success_com_cota(self, template):
        """Test successful validation with cota field."""
        dados = {
            "uf": "SP",
            "municipio": "7107",
            "codigoReceita": "0220",
            "codigoReceitaExtensao": "01",
            "tipoPA": "TR",
            "dataPA": "04/2021",
            "cota": "1",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2022-08-08T00:00:00",
            "observacao": "Darf calculado",
        }
        result = template.validate(dados)
        assert result == dados

    def test_validate_success_sem_uf_municipio(self, template):
        """Test successful validation without uf and municipio."""
        dados = {
            "codigoReceita": "1162",
            "codigoReceitaExtensao": "01",
            "tipoPA": "ME",
            "dataPA": "01/2022",
            "vencimento": "2022-02-18T00:00:00",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2022-08-08T00:00:00",
            "observacao": "Darf calculado",
        }
        result = template.validate(dados)
        assert result == dados

    def test_validate_missing_required_field(self, template):
        """Test validation fails when required field is missing."""
        dados = {
            "codigoReceita": "0190",
            # Missing other required fields
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "required" in str(exc_info.value).lower()

    def test_validate_empty_codigo_receita(self, template):
        """Test validation fails when codigoReceita is empty."""
        dados = {
            "codigoReceita": "",
            "codigoReceitaExtensao": "01",
            "tipoPA": "ME",
            "dataPA": "12/2017",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2022-08-08T00:00:00",
            "observacao": "Darf calculado",
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999", "tipo": 1}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999", "tipo": 1}

        dados = {
            "uf": "SP",
            "municipio": "7107",
            "codigoReceita": "0190",
            "codigoReceitaExtensao": "01",
            "tipoPA": "ME",
            "dataPA": "12/2017",
            "vencimento": "2018-01-31T00:00:00",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2022-08-08T00:00:00",
            "observacao": "Darf calculado",
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "SICALC"
        assert pedido_dados["idServico"] == "CONSOLIDARGERARDARF51"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("SICALC", "CONSOLIDARGERARDARF51")
        assert template_class is not None
        assert template_class == ConsolidarGerarDarf51Template


class TestGerarDarfCodBarra53Template:
    """Tests for GerarDarfCodBarra53Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return GerarDarfCodBarra53Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "SICALC"
        assert template.id_servico == "GERARDARFCODBARRA53"
        assert template.versao_sistema == "2.9"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Emitir"

    def test_validate_success_com_uf_municipio(self, template):
        """Test successful validation with uf and municipio."""
        dados = {
            "uf": "SP",
            "municipio": "7107",
            "codigoReceita": "6106",
            "codigoReceitaExtensao": "01",
            "tipoPA": "ME",
            "dataPA": "05/2005",
            "vencimento": "2005-06-10T00:00:00",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2024-03-25T00:00:00",
            "observacao": "Darf calculado",
            "confissao": False,
        }
        result = template.validate(dados)
        assert result == dados

    def test_validate_success_com_numero_referencia(self, template):
        """Test successful validation with numeroReferencia."""
        dados = {
            "codigoReceita": "1394",
            "codigoReceitaExtensao": "01",
            "tipoPA": "DI",
            "dataPA": "25/03/2024",
            "vencimento": "2024-03-25T00:00:00",
            "numeroReferencia": "8176000",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2024-03-25T00:00:00",
            "observacao": "Darf manual",
        }
        result = template.validate(dados)
        assert result == dados

    def test_validate_missing_required_field(self, template):
        """Test validation fails when required field is missing."""
        dados = {
            "codigoReceita": "1394",
            # Missing other required fields
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "required" in str(exc_info.value).lower()

    def test_validate_invalid_confissao_type(self, template):
        """Test validation fails when confissao is not boolean."""
        dados = {
            "codigoReceita": "6106",
            "codigoReceitaExtensao": "01",
            "tipoPA": "ME",
            "dataPA": "05/2005",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2024-03-25T00:00:00",
            "observacao": "Darf calculado",
            "confissao": "false",  # Should be bool, not str
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "boolean" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "99999999999999", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "99999999999999", "tipo": 2}

        dados = {
            "codigoReceita": "1394",
            "codigoReceitaExtensao": "01",
            "tipoPA": "DI",
            "dataPA": "25/03/2024",
            "vencimento": "2024-03-25T00:00:00",
            "numeroReferencia": "8176000",
            "valorImposto": "1000.00",
            "dataConsolidacao": "2024-03-25T00:00:00",
            "observacao": "Darf manual",
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "SICALC"
        assert pedido_dados["idServico"] == "GERARDARFCODBARRA53"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("SICALC", "GERARDARFCODBARRA53")
        assert template_class is not None
        assert template_class == GerarDarfCodBarra53Template


class TestConsultaApoioReceitas52Template:
    """Tests for ConsultaApoioReceitas52Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsultaApoioReceitas52Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "SICALC"
        assert template.id_servico == "CONSULTAAPOIORECEITAS52"
        assert template.versao_sistema == "2.9"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Apoiar"

    def test_validate_success(self, template):
        """Test successful validation with valid codigoReceita."""
        dados = {"codigoReceita": "6106"}
        result = template.validate(dados)
        assert result == dados

    def test_validate_missing_codigo_receita(self, template):
        """Test validation fails when codigoReceita is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "codigo" in str(exc_info.value).lower()

    def test_validate_empty_codigo_receita(self, template):
        """Test validation fails when codigoReceita is empty."""
        dados = {"codigoReceita": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "empty" in str(exc_info.value).lower()

    def test_validate_invalid_codigo_receita_type(self, template):
        """Test validation fails when codigoReceita is not a string."""
        dados = {"codigoReceita": 6106}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "string" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000", "tipo": 1}

        dados = {"codigoReceita": "6106"}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "SICALC"
        assert pedido_dados["idServico"] == "CONSULTAAPOIORECEITAS52"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("SICALC", "CONSULTAAPOIORECEITAS52")
        assert template_class is not None
        assert template_class == ConsultaApoioReceitas52Template


