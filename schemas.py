# schemas.py
# database schema classes for FastAPI

from pydantic import BaseModel, EmailStr

class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str

class Login(BaseModel):
    username: str
    password: str
