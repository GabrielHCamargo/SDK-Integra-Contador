"""Common Pydantic models for the SDK."""

from typing import Literal

from pydantic import BaseModel, Field


class Contratante(BaseModel):
    """Model for contratante (contractor)."""

    numero: str = Field(..., description="CNPJ or CPF number")
    tipo: Literal[1, 2] = Field(..., description="1 for CPF, 2 for CNPJ")


class Contribuinte(BaseModel):
    """Model for contribuinte (taxpayer)."""

    numero: str = Field(..., description="CNPJ or CPF number")
    tipo: Literal[1, 2] = Field(..., description="1 for CPF, 2 for CNPJ")


class AutorPedidoDados(BaseModel):
    """Model for autorPedidoDados (request author)."""

    numero: str = Field(..., description="CNPJ or CPF number")
    tipo: Literal[1, 2] = Field(..., description="1 for CPF, 2 for CNPJ")


class PedidoDados(BaseModel):
    """Base model for pedidoDados (request data)."""

    idSistema: str = Field(..., description="System ID")
    idServico: str = Field(..., description="Service ID")
    versaoSistema: str = Field(default="1.0", description="System version")
    dados: str = Field(..., description="Service-specific data as JSON string")

