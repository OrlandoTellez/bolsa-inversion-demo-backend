from fastapi import APIRouter, HTTPException, status
from typing import List
import random

from ..schemas.stock import StockResponse, StockHistoryResponse, StockHistoryPoint
from ..infrastructure.database import db

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get("", response_model=List[StockResponse])
async def get_all_stocks():
    """
    Get all available stocks.
    """
    stocks = db.get_all_stocks()
    return [
        StockResponse(
            ticker=s.ticker,
            company=s.company,
            price=s.price,
            change=s.change
        )
        for s in stocks
    ]


@router.get("/{ticker}", response_model=StockResponse)
async def get_stock(ticker: str):
    """
    Get a specific stock by ticker.
    """
    stock = db.get_stock(ticker.upper())
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {ticker} no encontrado"
        )
    
    return StockResponse(
        ticker=stock.ticker,
        company=stock.company,
        price=stock.price,
        change=stock.change
    )


@router.get("/{ticker}/history", response_model=StockHistoryResponse)
async def get_stock_history(ticker: str, months: int = 6):
    """
    Get price history for a stock.
    """
    stock = db.get_stock(ticker.upper())
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {ticker} no encontrado"
        )
    
    # Generate mock historical data
    months_names = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    current_month = 11  # December
    history = []
    
    price = stock.price * 0.85  # Start at 85% of current price
    for i in range(months):
        month_idx = (current_month - months + i + 1) % 12
        # Random walk
        price = price * (1 + random.uniform(-0.05, 0.08))
        history.append(StockHistoryPoint(
            date=months_names[month_idx],
            value=round(price, 2)
        ))
    
    # Add current price as last point
    history.append(StockHistoryPoint(
        date=months_names[current_month],
        value=stock.price
    ))
    
    return StockHistoryResponse(
        ticker=stock.ticker,
        company=stock.company,
        history=history
    )
