# database.py
# database configuration

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from rich.console import Console
import os

# Load the database URL from the .env file
console = Console()
load_dotenv()
SQLALCHEMY_DATABASE_FILENAME = os.getenv("SQLALCHEMY_DATABASE_FILENAME", "kcx.db")

# Use absolute path for Docker environment
if os.getenv("IS_IN_KCX_BACKEND_DOCKER", "false").lower() == "true":
    SQLALCHEMY_DATABASE_URL = f"sqlite:////app/data/database/{SQLALCHEMY_DATABASE_FILENAME}"
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///../data/database/{SQLALCHEMY_DATABASE_FILENAME}"

console.log(f"Database URL: [bold]{SQLALCHEMY_DATABASE_URL}[/bold]")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
console.log(f"[bold cyan]Database engine created: {engine} (DB: {engine.url.database})[/bold cyan]")

Base = declarative_base()
console.log(f"[bold cyan]Base class created[/bold cyan]")
