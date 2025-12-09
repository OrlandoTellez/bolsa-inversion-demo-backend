from pydantic import BaseModel
from typing import List


class HoldingResponse(BaseModel):
    """Schema for a portfolio holding."""
    ticker: str
    company: str
    shares: int
    avgPrice: float
    currentPrice: float
    purchaseDate: str


class BalanceResponse(BaseModel):
    """Schema for cash balance."""
    balance: float


class PortfolioSummary(BaseModel):
    """Schema for portfolio summary."""
    totalValue: float
    totalInvested: float
    totalGainLoss: float
    totalGainLossPercent: float
    balance: float
    holdings: List[HoldingResponse]
