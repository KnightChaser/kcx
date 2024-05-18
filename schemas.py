# schemas.py
# database schema classes for FastAPI

from pydantic import BaseModel, EmailStr, FiniteFloat, Field

# User registration schema
class UserRegistrationSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# User login schema
class LoginSchema(BaseModel):
    username: str
    password: str

# User balance schema
class BalanceSchema(BaseModel):
    KRW: FiniteFloat
    BTC: FiniteFloat
    ETH: FiniteFloat
    XRP: FiniteFloat

# User balance schema for deposit and withdraw
class BalanceDepositWithdrawSchema(BaseModel):
    KRW: FiniteFloat = Field(..., gt=0, description="Amount of KRW to deposit or withdraw, must be greater than zero")

# User buy/sell cryptocurrency schema
class BuyCryptoSchema(BaseModel):
    market_code:        str
    amount:             FiniteFloat

class SellCryptoSchema(BaseModel):
    market_code:        str
    amount:             FiniteFloat

# User trading history schema
class TradeHistorySchema(BaseModel):
    currency:           str
    amount:             FiniteFloat
    price:              FiniteFloat
    transaction_type:   str
    leverage_ratio:     FiniteFloat