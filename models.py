# models.py
# ORM classes for FastAPI

from sqlalchemy import Column, Integer, Float, String, DateTime, func, ForeignKey
from database import Base

# User credentials
class User(Base):
    __tablename__   = "users"
    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True, index=True)
    username        = Column(String, unique=True, index=True)
    password        = Column(String)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

# User balance in their account, connected to the User table
class Balance(Base):
    __tablename__   = "balances"
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"))
    KRW             = Column(Float, default=0)        # South Korean Won (fiat currency)
    BTC             = Column(Float, default=0)        # Bitcoin
    ETH             = Column(Float, default=0)        # Ethereum
    XRP             = Column(Float, default=0)        # Ripple
    created_at      = Column(DateTime(timezone=True), server_default=func.now())