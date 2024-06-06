# api/statistics/statistics.py
# API routers for this service's statistics data

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Dict
from database_session import get_redis_db

router: APIRouter = APIRouter()

# Get the statistics data of the total amount of cryptocurrency traded
@router.get("/api/statistics/total-transaction-amount")
async def get_total_transactions(redis_client = Depends(get_redis_db)) -> JSONResponse:
    try:
        keys = redis_client.keys("total_transaction_amount:*")
        total_transactions: Dict[str, float] = {}
        for key in keys:
            market_code = key.decode("utf-8").split(":")[1]
            total_amount = float(redis_client.get(key))
            total_transactions[market_code] = total_amount
        return JSONResponse(content=total_transactions, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
