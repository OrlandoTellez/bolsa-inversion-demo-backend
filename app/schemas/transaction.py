from pydantic import BaseModel
from typing import Literal


class TransactionCreate(BaseModel):
    """Schema for creating a transaction (buy/sell)."""
    ticker: str
    shares: int
    bank: str


class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: str
    type: Literal["compra", "venta"]
    ticker: str
    company: str
    shares: int
    price: float
    total: float
    date: str
    bank: str
