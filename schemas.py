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
    AAVE: FiniteFloat
    ADA: FiniteFloat
    AVAX: FiniteFloat
    BAT: FiniteFloat
    BCH: FiniteFloat
    BTC: FiniteFloat
    BTG: FiniteFloat
    BTT: FiniteFloat
    DOT: FiniteFloat
    EOS: FiniteFloat
    ETC: FiniteFloat
    ETH: FiniteFloat
    HBAR: FiniteFloat
    LINK: FiniteFloat
    MANA: FiniteFloat
    MATIC: FiniteFloat
    NEAR: FiniteFloat
    NEO: FiniteFloat
    ONT: FiniteFloat
    QTUM: FiniteFloat
    SAND: FiniteFloat
    SBD: FiniteFloat
    SC: FiniteFloat
    SHIB: FiniteFloat
    SOL: FiniteFloat
    STORJ: FiniteFloat
    STRAX: FiniteFloat
    SUI: FiniteFloat
    TFUEL: FiniteFloat
    THETA: FiniteFloat
    TRX: FiniteFloat
    VET: FiniteFloat
    WAVES: FiniteFloat
    XEC: FiniteFloat
    XEM: FiniteFloat
    XLM: FiniteFloat
    XRP: FiniteFloat
    XTZ: FiniteFloat

    AAVE_average_unit_price: FiniteFloat
    ADA_average_unit_price: FiniteFloat
    AVAX_average_unit_price: FiniteFloat
    BAT_average_unit_price: FiniteFloat
    BCH_average_unit_price: FiniteFloat
    BTC_average_unit_price: FiniteFloat
    BTG_average_unit_price: FiniteFloat
    BTT_average_unit_price: FiniteFloat
    DOT_average_unit_price: FiniteFloat
    EOS_average_unit_price: FiniteFloat
    ETC_average_unit_price: FiniteFloat
    ETH_average_unit_price: FiniteFloat
    HBAR_average_unit_price: FiniteFloat
    LINK_average_unit_price: FiniteFloat
    MANA_average_unit_price: FiniteFloat
    MATIC_average_unit_price: FiniteFloat
    NEAR_average_unit_price: FiniteFloat
    NEO_average_unit_price: FiniteFloat
    ONT_average_unit_price: FiniteFloat
    QTUM_average_unit_price: FiniteFloat
    SAND_average_unit_price: FiniteFloat
    SBD_average_unit_price: FiniteFloat
    SC_average_unit_price: FiniteFloat
    SHIB_average_unit_price: FiniteFloat
    SOL_average_unit_price: FiniteFloat
    STORJ_average_unit_price: FiniteFloat
    STRAX_average_unit_price: FiniteFloat
    SUI_average_unit_price: FiniteFloat
    TFUEL_average_unit_price: FiniteFloat
    THETA_average_unit_price: FiniteFloat
    TRX_average_unit_price: FiniteFloat
    VET_average_unit_price: FiniteFloat
    WAVES_average_unit_price: FiniteFloat
    XEC_average_unit_price: FiniteFloat
    XEM_average_unit_price: FiniteFloat
    XLM_average_unit_price: FiniteFloat
    XRP_average_unit_price: FiniteFloat
    XTZ_average_unit_price: FiniteFloat

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