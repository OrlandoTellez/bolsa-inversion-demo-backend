from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
import uuid

from ..schemas.transaction import TransactionCreate, TransactionResponse
from ..core.security import get_current_user_id
from ..infrastructure.database import db
from ..domain.models import Transaction, Holding

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=List[TransactionResponse])
async def get_transactions(user_id: str = Depends(get_current_user_id)):
    """
    Get all transactions for the current user.
    """
    transactions = db.get_transactions(user_id)
    return [
        TransactionResponse(
            id=t.id,
            type=t.type,
            ticker=t.ticker,
            company=t.company,
            shares=t.shares,
            price=t.price,
            total=t.total,
            date=t.date,
            bank=t.bank
        )
        for t in transactions
    ]


@router.post("/buy", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def buy_stock(data: TransactionCreate, user_id: str = Depends(get_current_user_id)):
    """
    Buy shares of a stock.
    """
    # Get stock
    stock = db.get_stock(data.ticker.upper())
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {data.ticker} no encontrado"
        )
    
    # Get portfolio
    portfolio = db.get_portfolio(user_id)
    if not portfolio:
        # Auto-create portfolio for demo resilience
        from ..domain.models import Portfolio
        portfolio = Portfolio(user_id=user_id, balance=1000.0)
        db.update_portfolio(portfolio)
    
    # Calculate total cost
    total = stock.price * data.shares
    
    # Check balance
    if total > portfolio.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Saldo insuficiente. Disponible: C$ {portfolio.balance:.2f}, Requerido: C$ {total:.2f}"
        )
    
    # Update balance
    portfolio.balance -= total
    
    # Update or create holding
    existing_holding = None
    for h in portfolio.holdings:
        if h.ticker == stock.ticker:
            existing_holding = h
            break
    
    if existing_holding:
        # Calculate new average price
        new_total_shares = existing_holding.shares + data.shares
        new_avg_price = (
            (existing_holding.shares * existing_holding.avg_price) + 
            (data.shares * stock.price)
        ) / new_total_shares
        
        existing_holding.shares = new_total_shares
        existing_holding.avg_price = new_avg_price
        existing_holding.current_price = stock.price
    else:
        # Create new holding
        new_holding = Holding(
            ticker=stock.ticker,
            company=stock.company,
            shares=data.shares,
            avg_price=stock.price,
            current_price=stock.price,
            purchase_date=datetime.now().strftime("%Y-%m-%d")
        )
        portfolio.holdings.append(new_holding)
    
    # Save portfolio
    db.update_portfolio(portfolio)
    
    # Create transaction
    transaction = Transaction(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type="compra",
        ticker=stock.ticker,
        company=stock.company,
        shares=data.shares,
        price=stock.price,
        total=total,
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        bank=data.bank
    )
    db.add_transaction(transaction)
    
    return TransactionResponse(
        id=transaction.id,
        type=transaction.type,
        ticker=transaction.ticker,
        company=transaction.company,
        shares=transaction.shares,
        price=transaction.price,
        total=transaction.total,
        date=transaction.date,
        bank=transaction.bank
    )


@router.post("/sell", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def sell_stock(data: TransactionCreate, user_id: str = Depends(get_current_user_id)):
    """
    Sell shares of a stock.
    """
    # Get stock
    stock = db.get_stock(data.ticker.upper())
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {data.ticker} no encontrado"
        )
    
    # Get portfolio
    portfolio = db.get_portfolio(user_id)
    if not portfolio:
        # Auto-create portfolio for demo resilience
        from ..domain.models import Portfolio
        portfolio = Portfolio(user_id=user_id, balance=1000.0)
        db.update_portfolio(portfolio)
    
    # Find holding
    holding = None
    holding_idx = -1
    for i, h in enumerate(portfolio.holdings):
        if h.ticker == stock.ticker:
            holding = h
            holding_idx = i
            break
    
    if not holding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No posees acciones de {stock.ticker}"
        )
    
    if data.shares > holding.shares:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solo tienes {holding.shares} acciones disponibles"
        )
    
    # Calculate sale value
    total = stock.price * data.shares
    
    # Update balance
    portfolio.balance += total
    
    # Update holding
    if data.shares == holding.shares:
        # Remove holding completely
        portfolio.holdings.pop(holding_idx)
    else:
        holding.shares -= data.shares
    
    # Save portfolio
    db.update_portfolio(portfolio)
    
    # Create transaction
    transaction = Transaction(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type="venta",
        ticker=stock.ticker,
        company=stock.company,
        shares=data.shares,
        price=stock.price,
        total=total,
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        bank=data.bank
    )
    db.add_transaction(transaction)
    
    return TransactionResponse(
        id=transaction.id,
        type=transaction.type,
        ticker=transaction.ticker,
        company=transaction.company,
        shares=transaction.shares,
        price=transaction.price,
        total=transaction.total,
        date=transaction.date,
        bank=transaction.bank
    )
