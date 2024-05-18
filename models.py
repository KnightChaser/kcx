# models.py
# ORM classes for FastAPI

from sqlalchemy import Column, Integer, Float, String, DateTime, func, ForeignKey
from database import Base

# User credentials
class User(Base):
    __tablename__           = "users"
    id                      = Column(Integer, primary_key=True, index=True)
    uuid                    = Column(String, unique=True, index=True)       # A unique identifier for the user and that is not guessable
    email                   = Column(String, unique=True, index=True)
    username                = Column(String, unique=True, index=True)
    password                = Column(String)
    created_at              = Column(DateTime(timezone=True), server_default=func.now())

# User balance in their account, connected to the User table
class Balance(Base):
    __tablename__           = "balances"
    id                      = Column(Integer, primary_key=True, index=True)
    user_id                 = Column(Integer, ForeignKey("users.id"))
    KRW                     = Column(Float, default=0)        # South Korean Won (fiat currency)
    ADA                     = Column(Float, default=0)        # Cardano
    AVAX                    = Column(Float, default=0)        # Avalanche
    BCH                     = Column(Float, default=0)        # Bitcoin Cash
    BTC                     = Column(Float, default=0)        # Bitcoin
    DOT                     = Column(Float, default=0)        # Polkadot
    ETC                     = Column(Float, default=0)        # Ethereum Classic
    ETH                     = Column(Float, default=0)        # Ethereum
    HBAR                    = Column(Float, default=0)        # Hedera Hashgraph
    LINK                    = Column(Float, default=0)        # Chainlink
    MATIC                   = Column(Float, default=0)        # Polygon
    NEAR                    = Column(Float, default=0)        # NEAR Protocol
    SHIB                    = Column(Float, default=0)        # Shiba Inu
    SOL                     = Column(Float, default=0)        # Solana
    TRX                     = Column(Float, default=0)        # TRON
    XEC                     = Column(Float, default=0)        # eCash
    XRP                     = Column(Float, default=0)        # Ripple

    ADA_average_unit_price  = Column(Float, default=0)        # Average unit price of ADA(Cardano)
    AVAX_average_unit_price = Column(Float, default=0)        # Average unit price of AVAX(Avalanche)
    BCH_average_unit_price  = Column(Float, default=0)        # Average unit price of BCH(Bitcoin Cash)
    BTC_average_unit_price  = Column(Float, default=0)        # Average unit price of BTC(Bitcoin)
    DOT_average_unit_price  = Column(Float, default=0)        # Average unit price of DOT(Polkadot)
    ETC_average_unit_price  = Column(Float, default=0)        # Average unit price of ETC(Ethereum Classic)
    ETH_average_unit_price  = Column(Float, default=0)        # Average unit price of ETH(Ethereum)
    HBAR_average_unit_price = Column(Float, default=0)        # Average unit price of HBAR(Hedera Hashgraph)
    LINK_average_unit_price = Column(Float, default=0)        # Average unit price of LINK(Chainlink)
    MATIC_average_unit_price= Column(Float, default=0)        # Average unit price of MATIC(Polygon)
    NEAR_average_unit_price = Column(Float, default=0)        # Average unit price of NEAR(NEAR Protocol)
    SHIB_average_unit_price = Column(Float, default=0)        # Average unit price of SHIB(Shiba Inu)
    SOL_average_unit_price  = Column(Float, default=0)        # Average unit price of SOL(Solana)
    TRX_average_unit_price  = Column(Float, default=0)        # Average unit price of TRX(TRON)
    XEC_average_unit_price  = Column(Float, default=0)        # Average unit price of XEC(eCash)
    XRP_average_unit_price  = Column(Float, default=0)        # Average unit price of XRP(Ripple)

    created_at              = Column(DateTime(timezone=True), server_default=func.now())

# User money deposit and withdraw history, connected to the User table
class DepositWithdrawHistory(Base):
    __tablename__           = "deposit_withdraw_history"
    id                      = Column(Integer, primary_key=True, index=True)
    user_id                 = Column(Integer, ForeignKey("users.id"))
    currency                = Column(String)                   # Currency type (KRW, BTC, ETH, XRP)
    amount                  = Column(Float)                    # Amount of money
    transaction_type        = Column(String)                   # Transaction type (deposit, withdraw)
    created_at              = Column(DateTime(timezone=True), server_default=func.now())

# User trading history, connected to the User table
class TradeHistory(Base):
    __tablename__           = "trade_history"
    id                      = Column(Integer, primary_key=True, index=True)
    user_id                 = Column(Integer, ForeignKey("users.id"))
    currency                = Column(String)                   # Currency type (BTC, ETH, XRP, ...)
    amount                  = Column(Float)                    # Amount of currency
    price                   = Column(Float)                    # Price(value) of the currency in KRW(fiat currency)
    transaction_type        = Column(String)                   # Transaction type (buy, sell)
    leverage_ratio          = Column(Float)                    # Leverage ratio (1, 2, 3, ...) (Leverage trading is not supported in this project for now, future work)
    created_at              = Column(DateTime(timezone=True), server_default=func.now())
