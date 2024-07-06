# api/statistics/statistics.py
# API routers for this service's statistics data

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database_session import get_sqlite3_db, get_redis_db
from models import Statistics, TradeHistory
import json

router = APIRouter()

# Get the statistics data of the total amount of cryptocurrency traded
@router.get("/api/statistics/total-transaction-amount")
async def get_total_transactions(db: Session = Depends(get_sqlite3_db)) -> JSONResponse:
    try:
        statistics = db.query(Statistics).first()
        if not statistics:
            return JSONResponse(content={"KRW": 0.0}, status_code=200)
        
        total_transactions = {
            "KRW": statistics.total_transaction_amount
        }
        return JSONResponse(content=total_transactions, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
# Get the number of transactions made
@router.get("/api/statistics/total-transaction-count")
async def get_total_transaction_count(db: Session = Depends(get_sqlite3_db)) -> JSONResponse:
    try:
        # Get the number of rows in the transactions table
        total_transaction_count = db.query(TradeHistory).count()
        return JSONResponse(content={"count": total_transaction_count}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Get the statistics data of the user leaderboard
@router.get("/api/statistics/user-leaderboard")
async def get_user_leaderboard(redis_client = Depends(get_redis_db)) -> JSONResponse:
    try:
        # Fetch the leaderboard from Redis
        leaderboard_data = redis_client.get("user_leaderboard")
        if leaderboard_data is None:
            return JSONResponse(content={}, status_code=200)

        leaderboard = json.loads(leaderboard_data)
        return JSONResponse(content=leaderboard, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)