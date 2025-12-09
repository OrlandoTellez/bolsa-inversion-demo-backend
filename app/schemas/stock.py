from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class StockResponse(BaseModel):
    """Schema for stock data."""
    ticker: str
    company: str
    price: float
    change: float  # Percentage change


class StockHistoryPoint(BaseModel):
    """Single point in stock history."""
    date: str
    value: float


class StockHistoryResponse(BaseModel):
    """Schema for stock price history."""
    ticker: str
    company: str
    history: List[StockHistoryPoint]
