"""PAGTOWEB - Consultar templates."""

from datetime import datetime
from typing import Any

from integra_sdk.exceptions import ValidationError
from integra_sdk.templates.base import BaseTemplate
from integra_sdk.templates.registry import TemplateRegistry


class Pagamentos71Template(BaseTemplate):
    """Template for PAGAMENTOS71 - Consulta Pagamento.

    Supports multiple query types:
    - By intervaloDataArrecadacao
    - By codigoReceitaLista
    - By intervaloValorTotalDocumento
    """

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PAGTOWEB",
            id_servico="PAGAMENTOS71",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary. Must contain at least one of:
                - intervaloDataArrecadacao: dict with dataInicial and dataFinal (YYYY-MM-DD)
                - codigoReceitaLista: list of strings
                - intervaloValorTotalDocumento: dict with valorInicial and valorFinal
                Also supports:
                - primeiroDaPagina: int (default: 0)
                - tamanhoDaPagina: int (default: 100)

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        validated: dict[str, Any] = {}

        # At least one query parameter must be present
        has_intervalo_data = "intervaloDataArrecadacao" in dados
        has_codigo_receita = "codigoReceitaLista" in dados
        has_intervalo_valor = "intervaloValorTotalDocumento" in dados

        if not (has_intervalo_data or has_codigo_receita or has_intervalo_valor):
            raise ValidationError(
                "At least one of 'intervaloDataArrecadacao', 'codigoReceitaLista', "
                "or 'intervaloValorTotalDocumento' must be provided"
            )

        # Validate intervaloDataArrecadacao
        if has_intervalo_data:
            intervalo = dados["intervaloDataArrecadacao"]
            if not isinstance(intervalo, dict):
                raise ValidationError("Field 'intervaloDataArrecadacao' must be a dictionary")

            if "dataInicial" not in intervalo:
                raise ValidationError("Field 'intervaloDataArrecadacao.dataInicial' is required")
            data_inicial = intervalo["dataInicial"]
            if not isinstance(data_inicial, str):
                raise ValidationError("Field 'intervaloDataArrecadacao.dataInicial' must be a string")
            try:
                datetime.strptime(data_inicial, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(
                    "Field 'intervaloDataArrecadacao.dataInicial' must be in YYYY-MM-DD format"
                )

            if "dataFinal" not in intervalo:
                raise ValidationError("Field 'intervaloDataArrecadacao.dataFinal' is required")
            data_final = intervalo["dataFinal"]
            if not isinstance(data_final, str):
                raise ValidationError("Field 'intervaloDataArrecadacao.dataFinal' must be a string")
            try:
                datetime.strptime(data_final, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(
                    "Field 'intervaloDataArrecadacao.dataFinal' must be in YYYY-MM-DD format"
                )

            validated["intervaloDataArrecadacao"] = {
                "dataInicial": data_inicial,
                "dataFinal": data_final,
            }

        # Validate codigoReceitaLista
        if has_codigo_receita:
            codigos = dados["codigoReceitaLista"]
            if not isinstance(codigos, list):
                raise ValidationError("Field 'codigoReceitaLista' must be a list")
            if len(codigos) == 0:
                raise ValidationError("Field 'codigoReceitaLista' cannot be empty")
            for codigo in codigos:
                if not isinstance(codigo, str):
                    raise ValidationError("All items in 'codigoReceitaLista' must be strings")
                if not codigo.strip():
                    raise ValidationError("Items in 'codigoReceitaLista' cannot be empty")
            validated["codigoReceitaLista"] = [str(c).strip() for c in codigos]

        # Validate intervaloValorTotalDocumento
        if has_intervalo_valor:
            intervalo = dados["intervaloValorTotalDocumento"]
            if not isinstance(intervalo, dict):
                raise ValidationError("Field 'intervaloValorTotalDocumento' must be a dictionary")

            if "valorInicial" not in intervalo:
                raise ValidationError("Field 'intervaloValorTotalDocumento.valorInicial' is required")
            valor_inicial = intervalo["valorInicial"]
            if isinstance(valor_inicial, str):
                try:
                    valor_inicial = float(valor_inicial)
                except ValueError:
                    raise ValidationError(
                        "Field 'intervaloValorTotalDocumento.valorInicial' must be a valid number"
                    )
            if not isinstance(valor_inicial, (int, float)):
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorInicial' must be a number"
                )
            if valor_inicial < 0:
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorInicial' must be non-negative"
                )

            if "valorFinal" not in intervalo:
                raise ValidationError("Field 'intervaloValorTotalDocumento.valorFinal' is required")
            valor_final = intervalo["valorFinal"]
            if isinstance(valor_final, str):
                try:
                    valor_final = float(valor_final)
                except ValueError:
                    raise ValidationError(
                        "Field 'intervaloValorTotalDocumento.valorFinal' must be a valid number"
                    )
            if not isinstance(valor_final, (int, float)):
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorFinal' must be a number"
                )
            if valor_final < 0:
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorFinal' must be non-negative"
                )

            validated["intervaloValorTotalDocumento"] = {
                "valorInicial": float(valor_inicial),
                "valorFinal": float(valor_final),
            }

        # Validate pagination (optional)
        if "primeiroDaPagina" in dados:
            primeiro = dados["primeiroDaPagina"]
            if isinstance(primeiro, str):
                try:
                    primeiro = int(primeiro)
                except ValueError:
                    raise ValidationError("Field 'primeiroDaPagina' must be a valid integer")
            if not isinstance(primeiro, int):
                raise ValidationError("Field 'primeiroDaPagina' must be an integer")
            if primeiro < 0:
                raise ValidationError("Field 'primeiroDaPagina' must be non-negative")
            validated["primeiroDaPagina"] = primeiro
        else:
            validated["primeiroDaPagina"] = 0

        if "tamanhoDaPagina" in dados:
            tamanho = dados["tamanhoDaPagina"]
            if isinstance(tamanho, str):
                try:
                    tamanho = int(tamanho)
                except ValueError:
                    raise ValidationError("Field 'tamanhoDaPagina' must be a valid integer")
            if not isinstance(tamanho, int):
                raise ValidationError("Field 'tamanhoDaPagina' must be an integer")
            if tamanho <= 0:
                raise ValidationError("Field 'tamanhoDaPagina' must be positive")
            validated["tamanhoDaPagina"] = tamanho
        else:
            validated["tamanhoDaPagina"] = 100

        return validated

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


class ContaConsDocArrPg73Template(BaseTemplate):
    """Template for CONTACONSDOCARRPG73 - Conta Consulta Pagamento.

    Supports multiple query types:
    - By intervaloDataArrecadacao
    - By codigoReceitaLista
    - By intervaloValorTotalDocumento
    """

    def __init__(self):
        """Initialize template."""
        super().__init__(
            id_sistema="PAGTOWEB",
            id_servico="CONTACONSDOCARRPG73",
            versao_sistema="1.0",
        )

    def validate(self, dados: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize input data.

        Args:
            dados: Input data dictionary. Must contain at least one of:
                - intervaloDataArrecadacao: dict with dataInicial and dataFinal (YYYY-MM-DD)
                - codigoReceitaLista: list of strings
                - intervaloValorTotalDocumento: dict with valorInicial and valorFinal

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        validated: dict[str, Any] = {}

        # At least one query parameter must be present
        has_intervalo_data = "intervaloDataArrecadacao" in dados
        has_codigo_receita = "codigoReceitaLista" in dados
        has_intervalo_valor = "intervaloValorTotalDocumento" in dados

        if not (has_intervalo_data or has_codigo_receita or has_intervalo_valor):
            raise ValidationError(
                "At least one of 'intervaloDataArrecadacao', 'codigoReceitaLista', "
                "or 'intervaloValorTotalDocumento' must be provided"
            )

        # Validate intervaloDataArrecadacao
        if has_intervalo_data:
            intervalo = dados["intervaloDataArrecadacao"]
            if not isinstance(intervalo, dict):
                raise ValidationError("Field 'intervaloDataArrecadacao' must be a dictionary")

            if "dataInicial" not in intervalo:
                raise ValidationError("Field 'intervaloDataArrecadacao.dataInicial' is required")
            data_inicial = intervalo["dataInicial"]
            if not isinstance(data_inicial, str):
                raise ValidationError("Field 'intervaloDataArrecadacao.dataInicial' must be a string")
            try:
                datetime.strptime(data_inicial, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(
                    "Field 'intervaloDataArrecadacao.dataInicial' must be in YYYY-MM-DD format"
                )

            if "dataFinal" not in intervalo:
                raise ValidationError("Field 'intervaloDataArrecadacao.dataFinal' is required")
            data_final = intervalo["dataFinal"]
            if not isinstance(data_final, str):
                raise ValidationError("Field 'intervaloDataArrecadacao.dataFinal' must be a string")
            try:
                datetime.strptime(data_final, "%Y-%m-%d")
            except ValueError:
                raise ValidationError(
                    "Field 'intervaloDataArrecadacao.dataFinal' must be in YYYY-MM-DD format"
                )

            validated["intervaloDataArrecadacao"] = {
                "dataInicial": data_inicial,
                "dataFinal": data_final,
            }

        # Validate codigoReceitaLista
        if has_codigo_receita:
            codigos = dados["codigoReceitaLista"]
            if not isinstance(codigos, list):
                raise ValidationError("Field 'codigoReceitaLista' must be a list")
            if len(codigos) == 0:
                raise ValidationError("Field 'codigoReceitaLista' cannot be empty")
            for codigo in codigos:
                if not isinstance(codigo, str):
                    raise ValidationError("All items in 'codigoReceitaLista' must be strings")
                if not codigo.strip():
                    raise ValidationError("Items in 'codigoReceitaLista' cannot be empty")
            validated["codigoReceitaLista"] = [str(c).strip() for c in codigos]

        # Validate intervaloValorTotalDocumento
        if has_intervalo_valor:
            intervalo = dados["intervaloValorTotalDocumento"]
            if not isinstance(intervalo, dict):
                raise ValidationError("Field 'intervaloValorTotalDocumento' must be a dictionary")

            if "valorInicial" not in intervalo:
                raise ValidationError("Field 'intervaloValorTotalDocumento.valorInicial' is required")
            valor_inicial = intervalo["valorInicial"]
            if isinstance(valor_inicial, str):
                try:
                    valor_inicial = float(valor_inicial)
                except ValueError:
                    raise ValidationError(
                        "Field 'intervaloValorTotalDocumento.valorInicial' must be a valid number"
                    )
            if not isinstance(valor_inicial, (int, float)):
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorInicial' must be a number"
                )
            if valor_inicial < 0:
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorInicial' must be non-negative"
                )

            if "valorFinal" not in intervalo:
                raise ValidationError("Field 'intervaloValorTotalDocumento.valorFinal' is required")
            valor_final = intervalo["valorFinal"]
            if isinstance(valor_final, str):
                try:
                    valor_final = float(valor_final)
                except ValueError:
                    raise ValidationError(
                        "Field 'intervaloValorTotalDocumento.valorFinal' must be a valid number"
                    )
            if not isinstance(valor_final, (int, float)):
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorFinal' must be a number"
                )
            if valor_final < 0:
                raise ValidationError(
                    "Field 'intervaloValorTotalDocumento.valorFinal' must be non-negative"
                )

            validated["intervaloValorTotalDocumento"] = {
                "valorInicial": float(valor_inicial),
                "valorFinal": float(valor_final),
            }

        return validated

    def get_endpoint(self) -> str:
        """Get the API endpoint."""
        return "Consultar"


# Register templates
TemplateRegistry.register("PAGTOWEB", "PAGAMENTOS71", Pagamentos71Template)
TemplateRegistry.register("PAGTOWEB", "CONTACONSDOCARRPG73", ContaConsDocArrPg73Template)

