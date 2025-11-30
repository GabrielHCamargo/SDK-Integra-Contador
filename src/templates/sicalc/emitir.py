"""SICALC - Emitir templates."""

import json
from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class ConsolidarGerarDarf51Template(BaseTemplate):
    """Template for CONSOLIDARGERARDARF51 - Gerar DARF consolidado.

    Usado para:
    - DARF de Pessoa Física
    - DARF de Pessoa Jurídica de um débito com cotas
    - DARF de Pessoa Jurídica - com código de barras e com numeração - QRCODE
    """

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="SICALC",
            id_servico="CONSOLIDARGERARDARF51",
            versao_sistema="2.9",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - codigoReceita: str (receita code, e.g., "0190", "0220", "1162")
                - codigoReceitaExtensao: str (receita extension, e.g., "01")
                - tipoPA: str (type, e.g., "ME", "TR", "DI")
                - dataPA: str (period date, format MM/YYYY or DD/MM/YYYY)
                - valorImposto: str (tax value, e.g., "1000.00")
                - dataConsolidacao: str (consolidation date, ISO format)
                - observacao: str (observation)
                Optional fields:
                - uf: str (state, e.g., "SP")
                - municipio: str (city code, e.g., "7107")
                - vencimento: str (due date, ISO format)
                - cota: str (quota number, e.g., "1")

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = [
            "codigoReceita",
            "codigoReceitaExtensao",
            "tipoPA",
            "dataPA",
            "valorImposto",
            "dataConsolidacao",
            "observacao",
        ]
        self._validate_required_fields(dados, required_fields)

        # Validate codigoReceita
        if not isinstance(dados["codigoReceita"], str):
            raise ValidationError("Field 'codigoReceita' must be a string")
        if not dados["codigoReceita"]:
            raise ValidationError("Field 'codigoReceita' cannot be empty")

        # Validate codigoReceitaExtensao
        if not isinstance(dados["codigoReceitaExtensao"], str):
            raise ValidationError("Field 'codigoReceitaExtensao' must be a string")
        if not dados["codigoReceitaExtensao"]:
            raise ValidationError("Field 'codigoReceitaExtensao' cannot be empty")

        # Validate tipoPA
        if not isinstance(dados["tipoPA"], str):
            raise ValidationError("Field 'tipoPA' must be a string")
        if not dados["tipoPA"]:
            raise ValidationError("Field 'tipoPA' cannot be empty")

        # Validate dataPA
        if not isinstance(dados["dataPA"], str):
            raise ValidationError("Field 'dataPA' must be a string")
        if not dados["dataPA"]:
            raise ValidationError("Field 'dataPA' cannot be empty")

        # Validate valorImposto
        if not isinstance(dados["valorImposto"], str):
            raise ValidationError("Field 'valorImposto' must be a string")
        if not dados["valorImposto"]:
            raise ValidationError("Field 'valorImposto' cannot be empty")

        # Validate dataConsolidacao
        if not isinstance(dados["dataConsolidacao"], str):
            raise ValidationError("Field 'dataConsolidacao' must be a string")
        if not dados["dataConsolidacao"]:
            raise ValidationError("Field 'dataConsolidacao' cannot be empty")

        # Validate observacao
        if not isinstance(dados["observacao"], str):
            raise ValidationError("Field 'observacao' must be a string")

        # Validate optional fields if present
        if "uf" in dados and dados["uf"]:
            if not isinstance(dados["uf"], str):
                raise ValidationError("Field 'uf' must be a string")

        if "municipio" in dados and dados["municipio"]:
            if not isinstance(dados["municipio"], str):
                raise ValidationError("Field 'municipio' must be a string")

        if "vencimento" in dados and dados["vencimento"]:
            if not isinstance(dados["vencimento"], str):
                raise ValidationError("Field 'vencimento' must be a string")

        if "cota" in dados and dados["cota"]:
            if not isinstance(dados["cota"], str):
                raise ValidationError("Field 'cota' must be a string")

        return dados

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


class GerarDarfCodBarra53Template(BaseTemplate):
    """Template for GERARDARFCODBARRA53 - Gerar DARF com código de barras.

    Usado para:
    - DARF de Pessoa Jurídica - com código de barras
    - DARF de Pessoa Jurídica - manual - com código de barras
    """

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="SICALC",
            id_servico="GERARDARFCODBARRA53",
            versao_sistema="2.9",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary with required fields:
                - codigoReceita: str (receita code, e.g., "1394", "6106")
                - codigoReceitaExtensao: str (receita extension, e.g., "01")
                - tipoPA: str (type, e.g., "ME", "DI")
                - dataPA: str (period date, format MM/YYYY or DD/MM/YYYY)
                - valorImposto: str (tax value, e.g., "1000.00")
                - dataConsolidacao: str (consolidation date, ISO format)
                - observacao: str (observation)
                Optional fields:
                - uf: str (state, e.g., "SP")
                - municipio: str (city code, e.g., "7107")
                - vencimento: str (due date, ISO format)
                - numeroReferencia: str (reference number, e.g., "8176000")
                - confissao: bool (confession flag)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # Validate required fields
        required_fields = [
            "codigoReceita",
            "codigoReceitaExtensao",
            "tipoPA",
            "dataPA",
            "valorImposto",
            "dataConsolidacao",
            "observacao",
        ]
        self._validate_required_fields(dados, required_fields)

        # Validate codigoReceita
        if not isinstance(dados["codigoReceita"], str):
            raise ValidationError("Field 'codigoReceita' must be a string")
        if not dados["codigoReceita"]:
            raise ValidationError("Field 'codigoReceita' cannot be empty")

        # Validate codigoReceitaExtensao
        if not isinstance(dados["codigoReceitaExtensao"], str):
            raise ValidationError("Field 'codigoReceitaExtensao' must be a string")
        if not dados["codigoReceitaExtensao"]:
            raise ValidationError("Field 'codigoReceitaExtensao' cannot be empty")

        # Validate tipoPA
        if not isinstance(dados["tipoPA"], str):
            raise ValidationError("Field 'tipoPA' must be a string")
        if not dados["tipoPA"]:
            raise ValidationError("Field 'tipoPA' cannot be empty")

        # Validate dataPA
        if not isinstance(dados["dataPA"], str):
            raise ValidationError("Field 'dataPA' must be a string")
        if not dados["dataPA"]:
            raise ValidationError("Field 'dataPA' cannot be empty")

        # Validate valorImposto
        if not isinstance(dados["valorImposto"], str):
            raise ValidationError("Field 'valorImposto' must be a string")
        if not dados["valorImposto"]:
            raise ValidationError("Field 'valorImposto' cannot be empty")

        # Validate dataConsolidacao
        if not isinstance(dados["dataConsolidacao"], str):
            raise ValidationError("Field 'dataConsolidacao' must be a string")
        if not dados["dataConsolidacao"]:
            raise ValidationError("Field 'dataConsolidacao' cannot be empty")

        # Validate observacao
        if not isinstance(dados["observacao"], str):
            raise ValidationError("Field 'observacao' must be a string")

        # Validate optional fields if present
        if "uf" in dados and dados["uf"]:
            if not isinstance(dados["uf"], str):
                raise ValidationError("Field 'uf' must be a string")

        if "municipio" in dados and dados["municipio"]:
            if not isinstance(dados["municipio"], str):
                raise ValidationError("Field 'municipio' must be a string")

        if "vencimento" in dados and dados["vencimento"]:
            if not isinstance(dados["vencimento"], str):
                raise ValidationError("Field 'vencimento' must be a string")

        if "numeroReferencia" in dados and dados["numeroReferencia"]:
            if not isinstance(dados["numeroReferencia"], str):
                raise ValidationError("Field 'numeroReferencia' must be a string")

        if "confissao" in dados:
            if not isinstance(dados["confissao"], bool):
                raise ValidationError("Field 'confissao' must be a boolean")

        return dados

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Emitir"


# Register templates
TemplateRegistry.register("SICALC", "CONSOLIDARGERARDARF51", ConsolidarGerarDarf51Template)
TemplateRegistry.register("SICALC", "GERARDARFCODBARRA53", GerarDarfCodBarra53Template)


