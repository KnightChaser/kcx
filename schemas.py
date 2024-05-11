# schemas.py
# database schema classes for FastAPI

from pydantic import BaseModel, EmailStr, FiniteFloat

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