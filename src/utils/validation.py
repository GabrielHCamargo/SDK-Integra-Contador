"""Validation utilities."""

from typing import Any


def validate_cnpj_cpf(numero: str, tipo: int) -> bool:
    """Basic validation for CNPJ/CPF format.

    Args:
        numero: CNPJ or CPF number
        tipo: 1 for CPF, 2 for CNPJ

    Returns:
        True if format is valid
    """
    if tipo == 1:  # CPF
        # Remove non-digits
        digits = "".join(filter(str.isdigit, numero))
        return len(digits) == 11
    elif tipo == 2:  # CNPJ
        # Remove non-digits
        digits = "".join(filter(str.isdigit, numero))
        return len(digits) == 14
    return False

