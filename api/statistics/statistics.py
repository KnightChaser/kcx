# api/statistics/statistics.py
# API routers for this service's statistics data

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database_session import get_sqlite3_db
from models import Statistics

router: APIRouter = APIRouter()

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
