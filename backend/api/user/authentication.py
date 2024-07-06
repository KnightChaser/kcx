# api/user/authentication.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import jwt
import os
from typing import Dict, Union
from secrets import token_hex

from ..email.smtp import SMTP

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Global dictionaries to store email-verification code pairs and verification status
email_verification_codes = {}
email_verification_status = {}

# Model for email verification request
class EmailVerificationRequest(BaseModel):
    email: EmailStr

# Get the current username from the JWT token if it's valid
# Authorization: `Bearer ${localStorage.getItem("token")}`, where the token is a JWT token
def get_current_user(token: str = Depends(oauth2_scheme)) -> Union[HTTPException, str]:
    """
    Get the current username from the JWT token if it's valid.
    """
    try:
        payload: Dict = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return username

# Create the FastAPI router
router = APIRouter()

@router.post("/api/auth/send-verification-email", status_code=200)
async def send_verification_email(request: EmailVerificationRequest) -> Dict:
    """
    Send a verification email to the user
    """
    email = request.email
    verification_code = token_hex(4)  # Generate a random 8-character hexadecimal number
    email_verification_codes[email] = verification_code  # Store the verification code
    email_verification_status[email] = False  # Initially set verification status to False

    # Create the SMTP instance
    smtp = SMTP()
    subject = "Email Verification"
    body = f"Your verification code is: {verification_code}"

    try:
        # Send the email
        smtp.send_email(receiver_email=email, subject=subject, body=body, purpose="email verification")
        return {"message": "Verification email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to send email: {str(e)}")

@router.post("/api/auth/verify-email", status_code=200)
async def verify_email(request: Request) -> Dict:
    """
    Verify the email using the verification code
    """
    data = await request.json()
    email = data.get('email')
    code = data.get('code')

    if email in email_verification_codes and email_verification_codes[email] == code:
        email_verification_status[email] = True  # Update verification status to True
        del email_verification_codes[email]  # Remove the verified code
        return {"message": "Email verified successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code.")
