# schemas.py
# database schema classes for FastAPI

from pydantic import BaseModel, EmailStr

# User registration schema
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str

# User login schema
class Login(BaseModel):
    username: str
    password: str

# User balance schema
class Balance(BaseModel):
    KRW: float
    BTC: float
    ETH: float
    XRP: float