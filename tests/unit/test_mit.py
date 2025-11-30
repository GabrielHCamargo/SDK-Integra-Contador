"""Unit tests for MIT templates."""

from unittest.mock import MagicMock

import pytest

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.mit.declarar import Encapuracao314Template
from integra_sdk.templates.mit.apoiar import SituacaoEnc315Template
from integra_sdk.templates.mit.consultar import (
    ConsApuracao316Template,
    ListaApuracoes317Template,
)
from integra_sdk.templates.registry import TemplateRegistry


class TestEncapuracao314Template:
    """Tests for Encapuracao314Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return Encapuracao314Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "MIT"
        assert template.id_servico == "ENCAPURACAO314"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Declarar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {
            "PeriodoApuracao": {"MesApuracao": 1, "AnoApuracao": 2025},
            "DadosIniciais": {
                "SemMovimento": False,
                "QualificacaoPj": 1,
                "TributacaoLucro": 2,
            },
        }
        result = template.validate(dados)
        assert result["PeriodoApuracao"]["MesApuracao"] == 1
        assert result["PeriodoApuracao"]["AnoApuracao"] == 2025

    def test_validate_with_debitos(self, template):
        """Test successful validation with Debitos."""
        dados = {
            "PeriodoApuracao": {"MesApuracao": 1, "AnoApuracao": 2025},
            "DadosIniciais": {"SemMovimento": False},
            "Debitos": {
                "Irpj": {"ListaDebitos": [{"IdDebito": 1, "ValorDebito": 100.0}]}
            },
        }
        result = template.validate(dados)
        assert "Debitos" in result

    def test_validate_missing_periodo(self, template):
        """Test validation fails when PeriodoApuracao is missing."""
        dados = {"DadosIniciais": {}}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "PeriodoApuracao" in str(exc_info.value)

    def test_validate_missing_dados_iniciais(self, template):
        """Test validation fails when DadosIniciais is missing."""
        dados = {"PeriodoApuracao": {"MesApuracao": 1, "AnoApuracao": 2025}}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "DadosIniciais" in str(exc_info.value)

    def test_validate_invalid_mes(self, template):
        """Test validation fails when MesApuracao is invalid."""
        dados = {
            "PeriodoApuracao": {"MesApuracao": 13, "AnoApuracao": 2025},
            "DadosIniciais": {},
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "MesApuracao" in str(exc_info.value)

    def test_validate_invalid_ano(self, template):
        """Test validation fails when AnoApuracao is invalid."""
        dados = {
            "PeriodoApuracao": {"MesApuracao": 1, "AnoApuracao": 1800},
            "DadosIniciais": {},
        }
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "AnoApuracao" in str(exc_info.value)

    def test_validate_mes_as_string(self, template):
        """Test validation accepts mes as string."""
        dados = {
            "PeriodoApuracao": {"MesApuracao": "1", "AnoApuracao": 2025},
            "DadosIniciais": {},
        }
        result = template.validate(dados)
        assert result["PeriodoApuracao"]["MesApuracao"] == 1

    def test_validate_ano_as_string(self, template):
        """Test validation accepts ano as string."""
        dados = {
            "PeriodoApuracao": {"MesApuracao": 1, "AnoApuracao": "2025"},
            "DadosIniciais": {},
        }
        result = template.validate(dados)
        assert result["PeriodoApuracao"]["AnoApuracao"] == 2025

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {
            "PeriodoApuracao": {"MesApuracao": 1, "AnoApuracao": 2025},
            "DadosIniciais": {"SemMovimento": False},
        }
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "MIT"
        assert pedido_dados["idServico"] == "ENCAPURACAO314"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("MIT", "ENCAPURACAO314")
        assert template_class is not None
        assert template_class == Encapuracao314Template


class TestSituacaoEnc315Template:
    """Tests for SituacaoEnc315Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return SituacaoEnc315Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "MIT"
        assert template.id_servico == "SITUACAOENC315"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Apoiar"

    def test_validate_success(self, template):
        """Test successful validation with valid protocolo."""
        dados = {"protocoloEncerramento": "AuYb4wuDp0GvCij3GDOAsA=="}
        result = template.validate(dados)
        assert result["protocoloEncerramento"] == "AuYb4wuDp0GvCij3GDOAsA=="

    def test_validate_missing_protocolo(self, template):
        """Test validation fails when protocoloEncerramento is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "protocolo" in str(exc_info.value).lower()

    def test_validate_empty_protocolo(self, template):
        """Test validation fails when protocoloEncerramento is empty."""
        dados = {"protocoloEncerramento": ""}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "protocolo" in str(exc_info.value).lower()

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"protocoloEncerramento": "AuYb4wuDp0GvCij3GDOAsA=="}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "MIT"
        assert pedido_dados["idServico"] == "SITUACAOENC315"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("MIT", "SITUACAOENC315")
        assert template_class is not None
        assert template_class == SituacaoEnc315Template


class TestConsApuracao316Template:
    """Tests for ConsApuracao316Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ConsApuracao316Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "MIT"
        assert template.id_servico == "CONSAPURACAO316"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid IdApuracao."""
        dados = {"IdApuracao": 0}
        result = template.validate(dados)
        assert result["IdApuracao"] == 0

    def test_validate_id_as_string(self, template):
        """Test validation accepts IdApuracao as string."""
        dados = {"IdApuracao": "123"}
        result = template.validate(dados)
        assert result["IdApuracao"] == 123

    def test_validate_missing_id(self, template):
        """Test validation fails when IdApuracao is missing."""
        dados = {}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "IdApuracao" in str(exc_info.value)

    def test_validate_negative_id(self, template):
        """Test validation fails when IdApuracao is negative."""
        dados = {"IdApuracao": -1}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "IdApuracao" in str(exc_info.value)

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"IdApuracao": 0}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "MIT"
        assert pedido_dados["idServico"] == "CONSAPURACAO316"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("MIT", "CONSAPURACAO316")
        assert template_class is not None
        assert template_class == ConsApuracao316Template


class TestListaApuracoes317Template:
    """Tests for ListaApuracoes317Template."""

    @pytest.fixture
    def template(self):
        """Fixture creating a template instance."""
        return ListaApuracoes317Template()

    def test_init(self, template):
        """Test template initialization."""
        assert template.id_sistema == "MIT"
        assert template.id_servico == "LISTAAPURACOES317"
        assert template.versao_sistema == "1.0"

    def test_get_endpoint(self, template):
        """Test endpoint name."""
        assert template.get_endpoint() == "Consultar"

    def test_validate_success(self, template):
        """Test successful validation with valid dados."""
        dados = {"mesApuracao": 1, "anoApuracao": 2025, "situacaoApuracao": 3}
        result = template.validate(dados)
        assert result["mesApuracao"] == 1
        assert result["anoApuracao"] == 2025
        assert result["situacaoApuracao"] == 3

    def test_validate_missing_mes(self, template):
        """Test validation fails when mesApuracao is missing."""
        dados = {"anoApuracao": 2025, "situacaoApuracao": 3}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "mes" in str(exc_info.value).lower()

    def test_validate_missing_ano(self, template):
        """Test validation fails when anoApuracao is missing."""
        dados = {"mesApuracao": 1, "situacaoApuracao": 3}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_missing_situacao(self, template):
        """Test validation fails when situacaoApuracao is missing."""
        dados = {"mesApuracao": 1, "anoApuracao": 2025}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "situacao" in str(exc_info.value).lower()

    def test_validate_invalid_mes(self, template):
        """Test validation fails when mesApuracao is invalid."""
        dados = {"mesApuracao": 13, "anoApuracao": 2025, "situacaoApuracao": 3}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "mes" in str(exc_info.value).lower()

    def test_validate_invalid_ano(self, template):
        """Test validation fails when anoApuracao is invalid."""
        dados = {"mesApuracao": 1, "anoApuracao": 1800, "situacaoApuracao": 3}
        with pytest.raises(ValidationError) as exc_info:
            template.validate(dados)
        assert "ano" in str(exc_info.value).lower()

    def test_validate_string_values(self, template):
        """Test validation accepts string values and converts them."""
        dados = {"mesApuracao": "1", "anoApuracao": "2025", "situacaoApuracao": "3"}
        result = template.validate(dados)
        assert result["mesApuracao"] == 1
        assert result["anoApuracao"] == 2025
        assert result["situacaoApuracao"] == 3

    def test_build_request(self, template):
        """Test building complete request."""
        config = MagicMock()
        config.contratante.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}
        config.autorPedidoDados.model_dump.return_value = {"cpfCnpj": "00000000000000", "tipo": 2}
        config.contribuinte.model_dump.return_value = {"numero": "00000000000000", "tipo": 2}

        dados = {"mesApuracao": 1, "anoApuracao": 2025, "situacaoApuracao": 3}
        request = template.build_request(config, dados)

        assert "pedidoDados" in request
        pedido_dados = request["pedidoDados"]
        assert pedido_dados["idSistema"] == "MIT"
        assert pedido_dados["idServico"] == "LISTAAPURACOES317"

    def test_template_registered(self):
        """Test that template is registered in TemplateRegistry."""
        template_class = TemplateRegistry.get("MIT", "LISTAAPURACOES317")
        assert template_class is not None
        assert template_class == ListaApuracoes317Template

