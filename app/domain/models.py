from dataclasses import dataclass, field
from typing import List, Literal
from datetime import datetime


@dataclass
class User:
    """User domain model."""
    id: str
    name: str
    email: str
    username: str
    password_hash: str
    role: Literal["admin", "user"] = "user"


@dataclass
class Stock:
    """Stock domain model."""
    ticker: str
    company: str
    price: float
    change: float  # Percentage change


@dataclass
class Holding:
    """Portfolio holding domain model."""
    ticker: str
    company: str
    shares: int
    avg_price: float
    current_price: float
    purchase_date: str


@dataclass
class Transaction:
    """Transaction domain model."""
    id: str
    user_id: str
    type: Literal["compra", "venta"]
    ticker: str
    company: str
    shares: int
    price: float
    total: float
    date: str
    bank: str


@dataclass
class Portfolio:
    """User portfolio domain model."""
    user_id: str
    balance: float = 1000.0
    holdings: List[Holding] = field(default_factory=list)
