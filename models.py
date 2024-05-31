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
    AAVE                    = Column(Float, default=0)        # Aave
    ADA                     = Column(Float, default=0)        # Cardano
    AVAX                    = Column(Float, default=0)        # Avalanche
    BAT                     = Column(Float, default=0)        # Basic Attention Token
    BCH                     = Column(Float, default=0)        # Bitcoin Cash
    BTC                     = Column(Float, default=0)        # Bitcoin
    BTG                     = Column(Float, default=0)        # Bitcoin Gold
    BTT                     = Column(Float, default=0)        # BitTorrent
    DOT                     = Column(Float, default=0)        # Polkadot
    EOS                     = Column(Float, default=0)        # EOS
    ETC                     = Column(Float, default=0)        # Ethereum Classic
    ETH                     = Column(Float, default=0)        # Ethereum
    HBAR                    = Column(Float, default=0)        # Hedera Hashgraph
    LINK                    = Column(Float, default=0)        # Chainlink
    MANA                    = Column(Float, default=0)        # Decentraland
    MATIC                   = Column(Float, default=0)        # Polygon
    NEAR                    = Column(Float, default=0)        # NEAR Protocol
    NEO                     = Column(Float, default=0)        # NEO
    ONT                     = Column(Float, default=0)        # Ontology
    QTUM                    = Column(Float, default=0)        # Quantum
    SAND                    = Column(Float, default=0)        # Sandbox
    SBD                     = Column(Float, default=0)        # Steem Dollars
    SC                      = Column(Float, default=0)        # Siacoin
    SHIB                    = Column(Float, default=0)        # Shiba Inu
    SOL                     = Column(Float, default=0)        # Solana
    STORJ                   = Column(Float, default=0)        # Storage
    STRAX                   = Column(Float, default=0)        # Stratis
    SUI                     = Column(Float, default=0)        # SUI
    TFUEL                   = Column(Float, default=0)        # Theta Fuel
    THETA                   = Column(Float, default=0)        # Theta Token
    TRX                     = Column(Float, default=0)        # TRON
    VET                     = Column(Float, default=0)        # VeChain
    WAVES                   = Column(Float, default=0)        # Waves
    XEC                     = Column(Float, default=0)        # eCash
    XEM                     = Column(Float, default=0)        # NEM
    XLM                     = Column(Float, default=0)        # Stellar Lumens
    XRP                     = Column(Float, default=0)        # Ripple
    XTZ                     = Column(Float, default=0)        # Tezos


    AAVE_average_unit_price     = Column(Float, default=0)    # Average unit price of AAVE(Aave)
    ADA_average_unit_price      = Column(Float, default=0)    # Average unit price of ADA(Cardano)
    AVAX_average_unit_price     = Column(Float, default=0)    # Average unit price of AVAX(Avalanche)
    BAT_average_unit_price      = Column(Float, default=0)    # Average unit price of BAT(Basic Attention Token)
    BCH_average_unit_price      = Column(Float, default=0)    # Average unit price of BCH(Bitcoin Cash)
    BTC_average_unit_price      = Column(Float, default=0)    # Average unit price of BTC(Bitcoin)
    BTG_average_unit_price      = Column(Float, default=0)    # Average unit price of BTG(Bitcoin Gold)
    BTT_average_unit_price      = Column(Float, default=0)    # Average unit price of BTT(BitTorrent)
    DOT_average_unit_price      = Column(Float, default=0)    # Average unit price of DOT(Polkadot)
    EOS_average_unit_price      = Column(Float, default=0)    # Average unit price of EOS
    ETC_average_unit_price      = Column(Float, default=0)    # Average unit price of ETC(Ethereum Classic)
    ETH_average_unit_price      = Column(Float, default=0)    # Average unit price of ETH(Ethereum)
    HBAR_average_unit_price     = Column(Float, default=0)    # Average unit price of HBAR(Hedera Hashgraph)
    LINK_average_unit_price     = Column(Float, default=0)    # Average unit price of LINK(Chainlink)
    MANA_average_unit_price     = Column(Float, default=0)    # Average unit price of MANA(Decentraland)
    MATIC_average_unit_price    = Column(Float, default=0)    # Average unit price of MATIC(Polygon)
    NEAR_average_unit_price     = Column(Float, default=0)    # Average unit price of NEAR(NEAR Protocol)
    NEO_average_unit_price      = Column(Float, default=0)    # Average unit price of NEO
    ONT_average_unit_price      = Column(Float, default=0)    # Average unit price of ONT(Ontology)
    QTUM_average_unit_price     = Column(Float, default=0)    # Average unit price of QTUM(Quantum)
    SAND_average_unit_price     = Column(Float, default=0)    # Average unit price of SAND(Sandbox)
    SBD_average_unit_price      = Column(Float, default=0)    # Average unit price of SBD(Steem Dollars)
    SC_average_unit_price       = Column(Float, default=0)    # Average unit price of SC(Siacoin)
    SHIB_average_unit_price     = Column(Float, default=0)    # Average unit price of SHIB(Shiba Inu)
    SOL_average_unit_price      = Column(Float, default=0)    # Average unit price of SOL(Solana)
    STORJ_average_unit_price    = Column(Float, default=0)    # Average unit price of STORJ(Storage)
    STRAX_average_unit_price    = Column(Float, default=0)    # Average unit price of STRAX(Stratis)
    SUI_average_unit_price      = Column(Float, default=0)    # Average unit price of SUI
    TFUEL_average_unit_price    = Column(Float, default=0)    # Average unit price of TFUEL(Theta Fuel)
    THETA_average_unit_price    = Column(Float, default=0)    # Average unit price of THETA(Theta Token)
    TRX_average_unit_price      = Column(Float, default=0)    # Average unit price of TRX(TRON)
    VET_average_unit_price      = Column(Float, default=0)    # Average unit price of VET(VeChain)
    WAVES_average_unit_price    = Column(Float, default=0)    # Average unit price of WAVES
    XEC_average_unit_price      = Column(Float, default=0)    # Average unit price of XEC(eCash)
    XEM_average_unit_price      = Column(Float, default=0)    # Average unit price of XEM(NEM)
    XLM_average_unit_price      = Column(Float, default=0)    # Average unit price of XLM(Stellar Lumens)
    XRP_average_unit_price      = Column(Float, default=0)    # Average unit price of XRP(Ripple)
    XTZ_average_unit_price      = Column(Float, default=0)    # Average unit price of XTZ(Tezos)

    created_at              = Column(DateTime(timezone=True), server_default=func.now())

# Market data for each currency.
# To resolve the API quota issue, the market data is stored in our database that offers a free API for this project.
# Periodically pulling the market data from the UPBIT exchange every

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
