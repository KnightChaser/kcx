# schemas.py
# database schema classes for FastAPI

from pydantic import BaseModel, EmailStr, NonNegativeFloat, PositiveFloat

class UserRegistrationSchema(BaseModel):
    """
    User registration request schema to this service
    """
    username: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    """
    User login request schema to this service
    """
    username: str
    password: str

class BalanceSchema(BaseModel):
    """
    User balance schema for deposit, withdraw, or check balance
    """
    KRW: NonNegativeFloat
    AAVE: NonNegativeFloat
    ADA: NonNegativeFloat
    AVAX: NonNegativeFloat
    BAT: NonNegativeFloat
    BCH: NonNegativeFloat
    BTC: NonNegativeFloat
    BTG: NonNegativeFloat
    BTT: NonNegativeFloat
    DOT: NonNegativeFloat
    EOS: NonNegativeFloat
    ETC: NonNegativeFloat
    ETH: NonNegativeFloat
    HBAR: NonNegativeFloat
    LINK: NonNegativeFloat
    MANA: NonNegativeFloat
    MATIC: NonNegativeFloat
    NEAR: NonNegativeFloat
    NEO: NonNegativeFloat
    ONT: NonNegativeFloat
    QTUM: NonNegativeFloat
    SAND: NonNegativeFloat
    SBD: NonNegativeFloat
    SC: NonNegativeFloat
    SHIB: NonNegativeFloat
    SOL: NonNegativeFloat
    STORJ: NonNegativeFloat
    STRAX: NonNegativeFloat
    SUI: NonNegativeFloat
    TFUEL: NonNegativeFloat
    THETA: NonNegativeFloat
    TRX: NonNegativeFloat
    VET: NonNegativeFloat
    WAVES: NonNegativeFloat
    XEC: NonNegativeFloat
    XEM: NonNegativeFloat
    XLM: NonNegativeFloat
    XRP: NonNegativeFloat
    XTZ: NonNegativeFloat

    AAVE_average_unit_price: NonNegativeFloat
    ADA_average_unit_price: NonNegativeFloat
    AVAX_average_unit_price: NonNegativeFloat
    BAT_average_unit_price: NonNegativeFloat
    BCH_average_unit_price: NonNegativeFloat
    BTC_average_unit_price: NonNegativeFloat
    BTG_average_unit_price: NonNegativeFloat
    BTT_average_unit_price: NonNegativeFloat
    DOT_average_unit_price: NonNegativeFloat
    EOS_average_unit_price: NonNegativeFloat
    ETC_average_unit_price: NonNegativeFloat
    ETH_average_unit_price: NonNegativeFloat
    HBAR_average_unit_price: NonNegativeFloat
    LINK_average_unit_price: NonNegativeFloat
    MANA_average_unit_price: NonNegativeFloat
    MATIC_average_unit_price: NonNegativeFloat
    NEAR_average_unit_price: NonNegativeFloat
    NEO_average_unit_price: NonNegativeFloat
    ONT_average_unit_price: NonNegativeFloat
    QTUM_average_unit_price: NonNegativeFloat
    SAND_average_unit_price: NonNegativeFloat
    SBD_average_unit_price: NonNegativeFloat
    SC_average_unit_price: NonNegativeFloat
    SHIB_average_unit_price: NonNegativeFloat
    SOL_average_unit_price: NonNegativeFloat
    STORJ_average_unit_price: NonNegativeFloat
    STRAX_average_unit_price: NonNegativeFloat
    SUI_average_unit_price: NonNegativeFloat
    TFUEL_average_unit_price: NonNegativeFloat
    THETA_average_unit_price: NonNegativeFloat
    TRX_average_unit_price: NonNegativeFloat
    VET_average_unit_price: NonNegativeFloat
    WAVES_average_unit_price: NonNegativeFloat
    XEC_average_unit_price: NonNegativeFloat
    XEM_average_unit_price: NonNegativeFloat
    XLM_average_unit_price: NonNegativeFloat
    XRP_average_unit_price: NonNegativeFloat
    XTZ_average_unit_price: NonNegativeFloat

class BalanceDepositWithdrawSchema(BaseModel):
    """
    User balance deposit or withdraw schema
    """
    KRW: PositiveFloat 

class BuyCryptoSchema(BaseModel):
    """
    User buy cryptocurrency schema
    """
    market_code:        str
    amount:             PositiveFloat

class SellCryptoSchema(BaseModel):
    """
    User sell cryptocurrency schema
    """
    market_code:        str
    amount:             PositiveFloat

class PasswordRecoveryRequestSchema(BaseModel):
    """
    User password recovery request schema
    """
    email: EmailStr
    new_password: str

class EmailChangeRequestSchema(BaseModel):
    """
    User email change request schema
    """
    old_email: EmailStr
    new_email: EmailStr

class PasswordChangeRequestSchema(BaseModel):
    """
    User change password request schema
    """
    old_password: str
    new_password: str