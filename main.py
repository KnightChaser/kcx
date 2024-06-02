# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.user.credentials import router as user_router
from api.user.balance import router as balance_router
from api.exchange.market import router as market_router
from api.exchange.trade import router as trade_router
from api.user.existence_check import check_existence
from api.user.password import password_hash

from tasks.fetch_and_store_market_data import start_fetch_and_store_market_data

from contextlib import asynccontextmanager
from rich.console import Console
from dotenv import load_dotenv
import os
import uuid

# Start this application when the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    console: Console = Console()

    # Load environment variables. So, we can use them in the application-wide
    load_dotenv()

    # Get Redis connection information from environment variables
    redis_host:str                  = os.getenv("REDIS_HOST", "db-redis")  # Use new service name
    redis_port:int                  = int(os.getenv("REDIS_PORT", 6379))
    redis_database:int              = int(os.getenv("REDIS_DB", 0))
    update_interval_in_seconds:int  = int(os.getenv("REDIS_UDPATE_INTERVAL_IN_SECONDS", 1))
    console.log(f"Setting up the Redis database at {redis_host}:{redis_port}/{redis_database} (update interval: {update_interval_in_seconds} seconds)")
    start_fetch_and_store_market_data(redis_host=redis_host, 
                                      redis_port=redis_port, 
                                      database=redis_database,
                                      update_interval_in_seconds=update_interval_in_seconds
                                      )

    # Create all tables in the database
    from database import Base, engine
    Base.metadata.create_all(bind=engine)

    # Create a test account if it doesn't exist
    test_account_id = os.getenv("TEST_ACCOUNT_ID", "test")
    test_account_pw = os.getenv("TEST_ACCOUNT_PW", "test")
    test_account_pw = password_hash(test_account_pw)
    test_account_email = os.getenv("TEST_ACCOUNT_EMAIL", "test@kcx.org")
    console.log(
        f"[bold green] Test account ID: {test_account_id}, PW: {os.getenv('TEST_ACCOUNT_PW')}(hashed: {test_account_pw}), Email: {test_account_email} [/bold green]")

    if check_existence(username=test_account_id, email=test_account_email):
        console.log("Test account already exists")
        yield
    else:
        # Create a test account, manually insert to the database
        from models import User
        from database import SessionLocal

        db = SessionLocal()
        user_uuid: str = str(uuid.uuid4())
        new_user = User(username=test_account_id,
                        email=test_account_email,
                        password=test_account_pw,
                        uuid=user_uuid)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        console.log(
            f"Test account created because it didn't exist [bold](UUID: {user_uuid})[/bold]")

        # Manually insert the balance for the test account
        from models import Balance
        db = SessionLocal()
        new_balance = Balance(user_id=new_user.id,
                              KRW=1000000)
        db.add(new_balance)
        db.commit()
        db.refresh(new_balance)
        db.close()
        console.log("Test account balance created")

        yield

app = FastAPI(lifespan=lifespan)

allowed_origins: list = [
    "http://localhost:5173",  # Vite dev server default
    "http://localhost:4173",  # Vite preview default
    "http://frontend:4173"    # Frontend service in Docker
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(balance_router)
app.include_router(market_router)
app.include_router(trade_router)
