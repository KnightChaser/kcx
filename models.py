# models.py
# ORM classes for FastAPI

from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class User(Base):
    __tablename__   = "users"
    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True, index=True)
    username        = Column(String, unique=True, index=True)
    password        = Column(String)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
