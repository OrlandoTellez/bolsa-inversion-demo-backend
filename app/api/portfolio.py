from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from ..schemas.portfolio import HoldingResponse, BalanceResponse, PortfolioSummary
from ..core.security import get_current_user_id
from ..infrastructure.database import db

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("", response_model=PortfolioSummary)
async def get_portfolio(user_id: str = Depends(get_current_user_id)):
    """
    Get user's complete portfolio summary.
    """
    portfolio = db.get_portfolio(user_id)
    if not portfolio:
        # Auto-create portfolio for demo resilience
        from ..domain.models import Portfolio
        portfolio = Portfolio(user_id=user_id, balance=1000.0)
        db.update_portfolio(portfolio)
    
    # Calculate totals
    holdings_response = []
    total_invested = 0
    total_value = 0
    
    for h in portfolio.holdings:
        # Update current price from stocks
        stock = db.get_stock(h.ticker)
        if stock:
            h.current_price = stock.price
        
        cost = h.shares * h.avg_price
        value = h.shares * h.current_price
        total_invested += cost
        total_value += value
        
        holdings_response.append(HoldingResponse(
            ticker=h.ticker,
            company=h.company,
            shares=h.shares,
            avgPrice=h.avg_price,
            currentPrice=h.current_price,
            purchaseDate=h.purchase_date
        ))
    
    total_gain_loss = total_value - total_invested
    total_gain_loss_percent = (total_gain_loss / total_invested * 100) if total_invested > 0 else 0
    
    return PortfolioSummary(
        totalValue=total_value,
        totalInvested=total_invested,
        totalGainLoss=total_gain_loss,
        totalGainLossPercent=total_gain_loss_percent,
        balance=portfolio.balance,
        holdings=holdings_response
    )


@router.get("/holdings", response_model=List[HoldingResponse])
async def get_holdings(user_id: str = Depends(get_current_user_id)):
    """
    Get user's current holdings.
    """
    portfolio = db.get_portfolio(user_id)
    if not portfolio:
        # Auto-create portfolio for demo resilience
        from ..domain.models import Portfolio
        portfolio = Portfolio(user_id=user_id, balance=1000.0)
        db.update_portfolio(portfolio)
    
    holdings_response = []
    for h in portfolio.holdings:
        # Update current price from stocks
        stock = db.get_stock(h.ticker)
        if stock:
            h.current_price = stock.price
        
        holdings_response.append(HoldingResponse(
            ticker=h.ticker,
            company=h.company,
            shares=h.shares,
            avgPrice=h.avg_price,
            currentPrice=h.current_price,
            purchaseDate=h.purchase_date
        ))
    
    return holdings_response


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(user_id: str = Depends(get_current_user_id)):
    """
    Get user's available cash balance.
    """
    portfolio = db.get_portfolio(user_id)
    if not portfolio:
        # Auto-create portfolio for demo resilience
        from ..domain.models import Portfolio
        portfolio = Portfolio(user_id=user_id, balance=1000.0)
        db.update_portfolio(portfolio)
    
    return BalanceResponse(balance=portfolio.balance)
