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
    ADA: FiniteFloat
    AVAX: FiniteFloat
    BCH: FiniteFloat
    BTC: FiniteFloat
    DOT: FiniteFloat
    ETC: FiniteFloat
    HBAR: FiniteFloat
    LINK: FiniteFloat
    MATIC: FiniteFloat
    NEAR: FiniteFloat
    SHIB: FiniteFloat
    SOL: FiniteFloat
    TRX: FiniteFloat
    XEC: FiniteFloat
    XRP: FiniteFloat

    ADA_average_unit_price: FiniteFloat
    AVAX_average_unit_price: FiniteFloat
    BCH_average_unit_price: FiniteFloat
    BTC_average_unit_price: FiniteFloat
    DOT_average_unit_price: FiniteFloat
    ETC_average_unit_price: FiniteFloat
    HBAR_average_unit_price: FiniteFloat
    LINK_average_unit_price: FiniteFloat
    MATIC_average_unit_price: FiniteFloat
    NEAR_average_unit_price: FiniteFloat
    SHIB_average_unit_price: FiniteFloat
    SOL_average_unit_price: FiniteFloat
    TRX_average_unit_price: FiniteFloat
    XEC_average_unit_price: FiniteFloat
    XRP_average_unit_price: FiniteFloat

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