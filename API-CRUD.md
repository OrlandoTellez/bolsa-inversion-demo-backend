# API Documentation - Bolsa de Inversiones Nicaragua

Base URL: `http://localhost:5050`

---

## 🔐 Authentication

### POST /auth/login
Authenticate user and get JWT token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "1",
    "name": "Administrador Demo",
    "email": "admin@bolsa.ni",
    "username": "admin",
    "role": "admin"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### POST /auth/register
Register a new user.

**Request Body:**
```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "username": "juanperez",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "id": "uuid-generated",
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "username": "juanperez",
  "role": "user"
}
```

---

### GET /auth/me
Get current authenticated user. **Requires Bearer Token.**

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": "1",
  "name": "Administrador Demo",
  "email": "admin@bolsa.ni",
  "username": "admin",
  "role": "admin"
}
```

---

## 📈 Stocks

### GET /stocks
List all available stocks.

**Response (200):**
```json
[
  {
    "ticker": "LAFISE",
    "company": "LAFISE Nicaragua",
    "price": 148.2,
    "change": 5.1
  },
  {
    "ticker": "BANCEN",
    "company": "Banco Central",
    "price": 96.8,
    "change": -3.5
  }
]
```

---

### GET /stocks/{ticker}
Get a specific stock by ticker.

**Example:** `GET /stocks/LAFISE`

**Response (200):**
```json
{
  "ticker": "LAFISE",
  "company": "LAFISE Nicaragua",
  "price": 148.2,
  "change": 5.1
}
```

---

### GET /stocks/{ticker}/history
Get price history for a stock.

**Query Parameters:**
- `months` (optional): Number of months of history (default: 6)

**Example:** `GET /stocks/LAFISE/history?months=6`

**Response (200):**
```json
{
  "ticker": "LAFISE",
  "company": "LAFISE Nicaragua",
  "history": [
    { "date": "Jul", "value": 125.50 },
    { "date": "Ago", "value": 130.20 },
    { "date": "Sep", "value": 135.80 },
    { "date": "Oct", "value": 140.10 },
    { "date": "Nov", "value": 145.30 },
    { "date": "Dic", "value": 148.20 }
  ]
}
```

---

## 💼 Portfolio

All portfolio endpoints **require Bearer Token**.

### GET /portfolio
Get complete portfolio summary.

**Response (200):**
```json
{
  "totalValue": 200000.50,
  "totalInvested": 180000.00,
  "totalGainLoss": 20000.50,
  "totalGainLossPercent": 11.11,
  "balance": 100000.00,
  "holdings": [
    {
      "ticker": "LAFISE",
      "company": "LAFISE Nicaragua",
      "shares": 500,
      "avgPrice": 140.5,
      "currentPrice": 148.2,
      "purchaseDate": "2024-01-10"
    }
  ]
}
```

---

### GET /portfolio/holdings
Get user's current holdings.

**Response (200):**
```json
[
  {
    "ticker": "LAFISE",
    "company": "LAFISE Nicaragua",
    "shares": 500,
    "avgPrice": 140.5,
    "currentPrice": 148.2,
    "purchaseDate": "2024-01-10"
  }
]
```

---

### GET /portfolio/balance
Get user's available cash balance.

**Response (200):**
```json
{
  "balance": 100000.00
}
```

---

## 💸 Transactions

All transaction endpoints **require Bearer Token**.

### GET /transactions
Get all user transactions.

**Response (200):**
```json
[
  {
    "id": "1",
    "type": "compra",
    "ticker": "LAFISE",
    "company": "LAFISE Nicaragua",
    "shares": 500,
    "price": 140.5,
    "total": 70250.00,
    "date": "2024-01-10 09:30",
    "bank": "BAC Nicaragua"
  }
]
```

---

### POST /transactions/buy
Buy shares of a stock.

**Request Body:**
```json
{
  "ticker": "LAFISE",
  "shares": 100,
  "bank": "BAC Nicaragua"
}
```

**Response (201):**
```json
{
  "id": "uuid-generated",
  "type": "compra",
  "ticker": "LAFISE",
  "company": "LAFISE Nicaragua",
  "shares": 100,
  "price": 148.2,
  "total": 14820.00,
  "date": "2024-12-08 20:15",
  "bank": "BAC Nicaragua"
}
```

**Error (400):** Insufficient balance
```json
{
  "detail": "Saldo insuficiente. Disponible: C$ 5000.00, Requerido: C$ 14820.00"
}
```

---

### POST /transactions/sell
Sell shares of a stock.

**Request Body:**
```json
{
  "ticker": "LAFISE",
  "shares": 50,
  "bank": "Banpro"
}
```

**Response (201):**
```json
{
  "id": "uuid-generated",
  "type": "venta",
  "ticker": "LAFISE",
  "company": "LAFISE Nicaragua",
  "shares": 50,
  "price": 148.2,
  "total": 7410.00,
  "date": "2024-12-08 20:15",
  "bank": "Banpro"
}
```

**Error (400):** Not enough shares
```json
{
  "detail": "Solo tienes 30 acciones disponibles"
}
```

---

## 🏥 Health Check

### GET /
API root endpoint.

**Response (200):**
```json
{
  "status": "ok",
  "message": "Bolsa de Inversiones Nicaragua API",
  "version": "1.0.0"
}
```

---

### GET /health
Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy"
}
```

---

## 🔑 Demo Users

| Username | Password | Role |
|----------|----------|------|
| `admin` or `admin@bolsa.ni` | `admin123` | admin |
| `usuario` or `usuario@bolsa.ni` | `usuario123` | user |

---

## 📌 Notes

- All authenticated endpoints require the `Authorization: Bearer <token>` header
- Prices are in Nicaraguan Córdobas (C$)
- Transaction types: `compra` (buy) / `venta` (sell)
- The `change` field in stocks represents percentage change
