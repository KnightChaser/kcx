# api/user/authentication.py
# API routers that check the user's authentication status (especially for JWT tokens)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from typing import Dict, Union

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authorization: `Bearer ${localStorage.getItem("token")}`, where the token is a JWT token
def get_current_user(token:str = Depends(oauth2_scheme)) -> Union[HTTPException, str]:
    try:
        payload:Dict = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        username:str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return username