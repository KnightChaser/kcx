# database.py
# database configuration

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from rich.console import Console
import os

# SQLite3 database file will be stored in the ./database directory.
# If there is no such directory, create one.
if not os.path.exists("database"):
    os.makedirs("database")

# Load the database URL from the .env file
console = Console()
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./database/kcx.db")
console.log(f"Database URL: [bold]{SQLALCHEMY_DATABASE_URL}[/bold]")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
console.log(f"[bold cyan]Database engine created: {engine} (DB: {engine.url.database})[/bold cyan]")

Base = declarative_base()
console.log(f"[bold cyan]Base class created[/bold cyan]")