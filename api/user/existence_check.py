# existence_check.py
# Check if the user exists in the database, based on the given criteria
# Internal use purposes only

from database import SessionLocal 

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from models import User

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Return boolean value if the user exists in the database
def check_existence(username:str, email:str) -> bool:
    db = SessionLocal()

    # If neither username nor email is provided, raise an exception
    if not username and not email:
        raise ValueError("Neither username nor email is provided")
    
    # If both username and email are provided, find the user by both criteria
    if username and email:
        user = db.query(User).filter(User.username == username, User.email == email).first()
        return True if user else False

    # If only username is provided, find the user by username
    if username:
        user = db.query(User).filter(User.username == username).first()
        return True if user else False
    if email:
        user = db.query(User).filter(User.email == email).first()
        return True if user else False
    
    return False