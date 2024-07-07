# api/user/credentials.py
# API routers for user login and registration (credentials)

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from schemas import LoginSchema, UserRegistrationSchema, PasswordRecoveryRequestSchema, EmailChangeRequestSchema
from typing import Dict, Union
from pathlib import Path
import filetype
import datetime
import jwt
import os
import uuid
import re

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from models import User, Balance
from api.user.password import password_hash, password_verify
from database_session import get_sqlite3_db
from .authentication import get_current_user, email_verification_status

# Create a JWT token (access token) for the user who logged in
def create_access_token(data: Dict, secret_key: str = None, expires_delta: datetime.timedelta = None) -> str:
    """
    Create a JWT token (access token) for the user who logged in
    """
    if not secret_key:
        raise ValueError("Secret key is missing")
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})  # Add the expiration time to the token
    encoded_jwt: str = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

# Get the user ID by the username (since the username is unique)
# For internal use only
def get_user_id_by_username(username: str, db: Session) -> Union[int, None]:
    """
    Get the user ID by the username (since the username is unique)
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user.id

router = APIRouter()

# Login router
@router.post("/api/account/login/")
def login(login: LoginSchema, db: Session = Depends(get_sqlite3_db)) -> Dict:
    """
    Handle user login and return JWT token
    """
    if not login.username or not login.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or password is missing")
    
    user = db.query(User).filter(User.username == login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not password_verify(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    secret_key: str = os.getenv("JWT_SECRET_KEY")
    access_token_expires_in_minutes: int = int(os.getenv("JWT_TOKEN_EXPIRES_MINUTES"))
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
    """
    Handle user registration
    """
    if not user.username or not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username, email, or password is missing")

    if not re.match("^[a-zA-Z0-9_]*$", user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username should contain only alphanumeric characters and underscores")

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    user.password = password_hash(user.password)

    new_user = User(
        uuid=str(uuid.uuid4()),  # UUID4 is used for the user ID(identifier)
        username=user.username,
        email=user.email,
        password=user.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_balance = Balance(
        user_id=new_user.id,
        KRW=int(os.getenv("STARTING_BALANCE_IN_KRW", 1000000))
    )
    db.add(new_balance)
    db.commit()
    db.refresh(new_balance)

    return {"id": new_user.id, 
            "username": new_user.username, 
            "email": new_user.email, 
            "created_at": new_user.created_at}

# Profile image upload router
@router.post("/api/account/upload-profile-image/")
async def upload_profile_image(current_user: User = Depends(get_current_user), file: UploadFile = File(...), db: Session = Depends(get_sqlite3_db)) -> Dict:
    """
    Upload a profile image for the current user
    """
    username: str = current_user["username"]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if os.getenv("IS_IN_KCX_BACKEND_DOCKER", "false").lower() == "true":
        upload_dir = Path("/app/data/uploads/profile_images")
    else:
        upload_dir = Path("../data/uploads/profile_images")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{username}.png"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    if not filetype.is_image(file_path):
        file_path.unlink()  # Delete the file
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file. Your file is now deleted. Please upload a valid image file.")

    return {"filename": str(file_path)}

# Profile image retrieval router (authentication is not required)
@router.post("/api/account/get-profile-image/")
async def get_profile_image(username: str = Form(...), db: Session = Depends(get_sqlite3_db)) -> FileResponse:
    """
    Retrieve a profile image for the specified username
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if os.getenv("IS_IN_KCX_BACKEND_DOCKER", "false").lower() == "true":
        image_directory = "/app/data/uploads/profile_images"
    else:
        image_directory = "../data/uploads/profile_images"
    file_path = Path(image_directory) / f"{username}.png"

    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile image not found")

    return FileResponse(path=file_path, media_type='image/png')

# Password recovery router
@router.post("/api/account/password-recovery", status_code=200)
async def password_recovery(request: PasswordRecoveryRequestSchema, db: Session = Depends(get_sqlite3_db)):
    """
    Reset the user's password if the email has been verified.
    """
    email = request.email
    new_password = request.new_password

    if email in email_verification_status and email_verification_status[email]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Hash the new password
        user.password = password_hash(new_password)
        db.commit()
        
        # Invalidate the verification status
        del email_verification_status[email]
        return {"message": "Password reset successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not verified.")

# Change email router
@router.post("/api/account/change-email", status_code=200)
async def change_email(request: EmailChangeRequestSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_sqlite3_db)):
    """
    Change the user's email if the email has been verified.
    """
    old_email = request.old_email
    new_email = request.new_email

    # Check if the old email is correct
    if old_email != current_user["email"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old email is incorrect.")

    user = db.query(User).filter(User.username == current_user["username"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Change the email if the new email is verified
    if new_email in email_verification_status and email_verification_status[new_email]:
        user.email = new_email
        db.commit()
        
        # Invalidate the verification status
        del email_verification_status[new_email]
        return {"message": "Email changed successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not verified.")
 