from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from rich.console import Console
from contextlib import asynccontextmanager
import bcrypt

# Database configuration
engine = create_engine('sqlite:///./test.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
Base.metadata.create_all(bind=engine)

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Login(BaseModel):
    username: str
    password: str

def hash_password(password) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# Create a test account when the server starts, using registration route
# Test account spec: username: test, email: test@kcx.org
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check if test account already exists
    console:Console = Console()
    db = SessionLocal()
    test_user = db.query(User).filter(User.username == "test").first()
    if test_user is None:
        # Create test account
        new_user = User(
            username = "test",
            email    = "test@kcx.org",
            password = hash_password("test"))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        console.log("[bold green]Test account created successfully![/bold green]")
    else:
        db.close()
        console.log("[bold yellow]Test account already exists![/bold yellow]")
    yield

app = FastAPI(lifespan = lifespan)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins       = ["*"],
    allow_credentials   = True,
    allow_methods       = ["*"],
    allow_headers       = ["*"],
)

# Routes to handle user registration and login
@app.post("/account/login/")
def login(login: Login, db: Session = Depends(get_db)):
    # Check if the parameters arrived correctly
    if not login.username or not login.password:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid username or password")

    user = db.query(User).filter(User.username == login.username).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid password")
    # Return 200 OK with user data
    return {"id": user.id, "username": user.username, "email": user.email, "created_at": user.created_at}

# Route to register a new user
@app.post("/account/register/")
def register(user_data: UserRegistration, db: Session = Depends(get_db)):
    # Check if email or username already exists
    existing_user = db.query(User).filter((User.username == user_data.username) | (User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Username or email already registered")

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create new user instance
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "created_at": new_user.created_at}
