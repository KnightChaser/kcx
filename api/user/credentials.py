# api/user/credentials.py
# API routers for user login and registration (credentials)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import Login, UserRegistration

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from models import User
from api.user.password import password_hash, password_verify
from database_session import get_db

router = APIRouter()

# Login router
@router.post("/account/login/")
def login(login: Login, db: Session = Depends(get_db)):
    # Check if the login information is arrived without any missing fields
    if not login.username or not login.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or password is missing")
    
    user = db.query(User).filter(User.username == login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not password_verify(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    # Login successful, send the user information
    return {"id": user.id, "username": user.username, "email": user.email}

# Register router
@router.post("/account/register/")
def register(user: UserRegistration, db: Session = Depends(get_db)):
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
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "created_at": new_user.created_at}