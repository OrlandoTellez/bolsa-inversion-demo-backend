"""
In-memory database for demo purposes.
In production, this would be replaced with SQLAlchemy + PostgreSQL/MySQL.
"""
from typing import Dict, List, Optional
from ..domain.models import User, Stock, Holding, Transaction, Portfolio


# Pre-computed bcrypt hashes for demo passwords to avoid slow initialization
# admin123 hash
ADMIN_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.J2LTMYq8GX6K9G"
# usuario123 hash  
USER_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.J2LTMYq8GX6K9G"


class InMemoryDatabase:
    """Simple in-memory database for demo."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.stocks: Dict[str, Stock] = {}
        self.portfolios: Dict[str, Portfolio] = {}
        self.transactions: List[Transaction] = []
        
        # Initialize with demo data
        self._init_demo_data()
    
    def _init_demo_data(self):
        """Initialize demo data."""
        # Demo users - using pre-computed hashes
        self.users["1"] = User(
            id="1",
            name="Administrador Demo",
            email="admin@bolsa.ni",
            username="admin",
            password_hash=ADMIN_HASH,
            role="admin"
        )
        self.users["2"] = User(
            id="2",
            name="Usuario Demo",
            email="usuario@bolsa.ni",
            username="usuario",
            password_hash=USER_HASH,
            role="user"
        )
        
        # Demo stocks - Nicaraguan companies
        self.stocks = {
            "LAFISE": Stock(ticker="LAFISE", company="LAFISE Nicaragua", price=148.2, change=5.1),
            "BANCEN": Stock(ticker="BANCEN", company="Banco Central", price=96.8, change=-3.5),
            "AGRI": Stock(ticker="AGRI", company="Agrícola Nicaragua", price=54.8, change=5.2),
            "ENITEL": Stock(ticker="ENITEL", company="ENITEL Telecom", price=80.5, change=2.0),
            "CEMEX": Stock(ticker="CEMEX", company="CEMEX Nicaragua", price=122.3, change=-2.8),
        }
        
        # Demo portfolios for each user
        for user_id in self.users:
            self.portfolios[user_id] = Portfolio(
                user_id=user_id,
                balance=1000.0,
                holdings=[
                    Holding(ticker="LAFISE", company="LAFISE Nicaragua", shares=50, 
                           avg_price=140.5, current_price=148.2, purchase_date="2024-01-10"),
                    Holding(ticker="BANCEN", company="Banco Central", shares=35,
                           avg_price=100.2, current_price=96.8, purchase_date="2023-12-15"),
                ]
            )
        
        # Demo transactions
        self.transactions = [
            Transaction(id="1", user_id="1", type="compra", ticker="LAFISE", company="LAFISE Nicaragua",
                       shares=500, price=140.5, total=70250, date="2024-01-10 09:30", bank="BAC Nicaragua"),
            Transaction(id="2", user_id="1", type="compra", ticker="BANCEN", company="Banco Central",
                       shares=350, price=100.2, total=35070, date="2023-12-15 14:20", bank="Banpro"),
            Transaction(id="3", user_id="1", type="compra", ticker="AGRI", company="Agrícola Nicaragua",
                       shares=800, price=52.0, total=41600, date="2024-01-05 10:15", bank="BAC Nicaragua"),
        ]
    
    # User methods
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username or user.email == username:
                return user
        return None
    
    def create_user(self, user: User) -> User:
        self.users[user.id] = user
        # Create empty portfolio for new user
        self.portfolios[user.id] = Portfolio(user_id=user.id)
        return user
    
    # Stock methods
    def get_all_stocks(self) -> List[Stock]:
        return list(self.stocks.values())
    
    def get_stock(self, ticker: str) -> Optional[Stock]:
        return self.stocks.get(ticker)
    
    # Portfolio methods
    def get_portfolio(self, user_id: str) -> Optional[Portfolio]:
        return self.portfolios.get(user_id)
    
    def update_portfolio(self, portfolio: Portfolio):
        self.portfolios[portfolio.user_id] = portfolio
    
    # Transaction methods
    def get_transactions(self, user_id: str) -> List[Transaction]:
        return [t for t in self.transactions if t.user_id == user_id]
    
    def add_transaction(self, transaction: Transaction):
        self.transactions.insert(0, transaction)


# Singleton database instance
db = InMemoryDatabase()
