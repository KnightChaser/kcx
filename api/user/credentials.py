# api/user/credentials.py
# API routers for user login and registration (credentials)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import LoginSchema, UserRegistrationSchema
from typing import Dict, Union
import datetime
import jwt
import os
import uuid

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from models import User, Balance
from api.user.password import password_hash, password_verify
from database_session import get_sqlite3_db

# Create a JWT token (access token) for the user who logged in
def create_access_token(data: Dict, secret_key:str = None, expires_delta: datetime.timedelta = None) -> str:
    # Check if the secret key is provided
    if not secret_key:
        raise ValueError("Secret key is missing")
    
    # Create the JWT token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes = expires_delta)
    to_encode.update({"exp": expire})       # Add the expiration time to the token
    encoded_jwt: str = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

# Get the user ID by the username (since the username is unique)
# For internal use only
def get_user_id_by_username(username:str, db:Session) -> Union[int | None]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user.id

router:APIRouter = APIRouter()

# Login router
@router.post("/api/account/login/")
def login(login: LoginSchema, db: Session = Depends(get_sqlite3_db)) -> Dict:
    # Check if the login information is arrived without any missing fields
    if not login.username or not login.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or password is missing")
    
    user = db.query(User).filter(User.username == login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not password_verify(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    # Login successful, send the user information
    secret_key:str = os.getenv("JWT_SECRET_KEY")
    access_token_expires_in_minutes:int = int(os.getenv("JWT_TOKEN_EXPIRES_MINUTES"))
    access_token = create_access_token(data={"sub": {
                                                "id": user.id, 
                                                "username": user.username, 
                                                "email": user.email
                                            }}, 
                                       secret_key=secret_key, 
                                       expires_delta=datetime.timedelta(minutes=access_token_expires_in_minutes))
    return {"access_token": access_token, 
            "token_type": "bearer",
            "username": user.username,
            "email": user.email,
            "uuid": user.uuid}

# Register router
@router.post("/api/account/register/")
def register(user: UserRegistrationSchema, db: Session = Depends(get_sqlite3_db)) -> Dict:
    # Check if the registration information is arrived without any missing fields
    if not user.username or not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username, email, or password is missing")
    
    # Check if the user already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    # Hash the password
    user.password = password_hash(user.password)

    # Create a new user instance
    new_user = User(
        uuid=str(uuid.uuid4()),       # UUID4 is used for the user ID(identifier)
        username=user.username,
        email=user.email,
        password=user.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Registration successful, charge initial fund 1,000,000 KRW to the user's account
    # Note that the initial fund is only for demonstration purposes
    new_balance = Balance(
        user_id=new_user.id,
        KRW=1000000
    )
    db.add(new_balance)
    db.commit()
    db.refresh(new_balance)

    # Send the user information
    return {"id": new_user.id, 
            "username": new_user.username, 
            "email": new_user.email, 
            "created_at": new_user.created_at}