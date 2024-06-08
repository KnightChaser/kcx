# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# API endpoints
from api.user.credentials import router as user_router
from api.user.balance import router as balance_router
from api.user.existence_check import check_existence
from api.user.password import password_hash
from api.statistics.statistics import router as service_statistics_router
from api.exchange.market import router as market_router
from api.exchange.trade import router as trade_router

# Tasks running in the background (multi-threading)
from tasks.fetch_and_store_market_data import start_fetch_and_store_market_data
from tasks.ranking_user_leaderboard import start_rank_user_leaderboard

from contextlib import asynccontextmanager
from rich.console import Console
from dotenv import load_dotenv
import os
import uuid
import redis

# Start this application when the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    console: Console = Console()

    # Load environment variables. So, we can use them in the application-wide
    load_dotenv()

    # Register service environment variables
    ALLOW_ARBITRARY_BALANCE_DEPOSIT = os.getenv("ALLOW_ARBITRARY_BALANCE_DEPOSIT", "false").lower() == "true"           # Can user deposit any amount of money?
    console.log(f"Allow arbitrary balance deposit: {ALLOW_ARBITRARY_BALANCE_DEPOSIT}")

    ALLOW_ARBITRARY_BALANCE_WITHDRAW = os.getenv("ALLOW_ARBITRARY_BALANCE_WITHDRAW", "false").lower() == "true"         # Can user withdraw any amount of money?
    console.log(f"Allow arbitrary balance withdraw: {ALLOW_ARBITRARY_BALANCE_WITHDRAW}")

    COMMON_STARTING_BALANCE_IN_KRW = int(os.getenv("COMMON_STARTING_BALANCE_IN_KRW", 1000000))                          # Common starting balance for all users
    console.log(f"Common starting balance in KRW: {COMMON_STARTING_BALANCE_IN_KRW}")

    # Check if the current environment is in Docker
    is_docker = os.getenv("IS_IN_KCX_BACKEND_DOCKER", "false").lower() == "true"
    console.log(f"Running in Docker: {is_docker}")

    # Manually set up the Redis client
    redis_host = "db-redis" if is_docker else "localhost"
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_database = int(os.getenv("REDIS_DB", 0))
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_database)
    console.log(f"Setting up the Redis database at {redis_host}:{redis_port}/{redis_database}")

    # Start the market data fetching and storing task (multi-threading)
    update_interval_in_seconds = int(os.getenv("REDIS_UDPATE_INTERVAL_IN_SECONDS", 1))
    start_fetch_and_store_market_data(redis_client=redis_client, update_interval_in_seconds=update_interval_in_seconds)
    console.log(f"Started fetching and storing the market data in the Redis database every {update_interval_in_seconds} seconds")

    # Start the user leaderboard ranking task (multi-threading)
    update_interval_in_seconds = int(os.getenv("USER_RANKING_UPDATE_INTERVAL_IN_SECONDS", 10))
    start_rank_user_leaderboard(update_interval_in_seconds=update_interval_in_seconds)
    console.log(f"Started ranking the user leaderboard every {update_interval_in_seconds} seconds")

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

# Hello world endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

allowed_origins: list = [
    # For localhost development
    "http://localhost:4173",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "https://localhost:4173",
    "https://localhost:5173",
    "https://localhost:8000",
    "https://127.0.0.1:4173",
    "https://127.0.0.1:5173",
    "https://127.0.0.1:8000",
    "https://kcx.knightchaser.com:4173",
    "https://kcx.knightchaser.com:5173",
    "https://kcx.knightchaser.com:8000",
    "https://frontend:4173",
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
app.include_router(service_statistics_router)