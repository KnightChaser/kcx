# api/exchange/market.py
# API routers for cryptocurrency market data (public)
# These API routers should be open to the public, no authentication required

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import json

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from models import Balance
from database_session import get_redis_db

router: APIRouter = APIRouter()

# Get the currently supported cryptocurrency list by this exchange
@router.get("/api/exchange/market/list")
def get_cryptocurrency_list() -> JSONResponse:
    # Available cryptocurrency lists are in the Balance model
    cryptocurrency_list = Balance.__table__.columns.keys()

    # Except for the
    # - id
    # - user_id
    # - created_at
    # - KRW (fiat currency)
    # - {market_code}_average_unit_price (average unit price of the cryptocurrency)
    cryptocurrency_list.remove("id")
    cryptocurrency_list.remove("user_id")
    cryptocurrency_list.remove("created_at")
    cryptocurrency_list.remove("KRW")
    for column in Balance.__table__.columns.keys():
        if column.endswith("_average_unit_price"):
            cryptocurrency_list.remove(column)

    return JSONResponse(content=cryptocurrency_list)

# Get the market data of the cryptocurrency from this Redis cache
@router.get("/api/exchange/market/ticker")
async def get_cryptocurrency_ticker(markets: str = None, redis_client=Depends(get_redis_db)) -> JSONResponse:
    if not markets:
        return JSONResponse(status_code=400, content="market_code_string is required")

    market_list: List[str] = markets.split(",")
    result: List[Dict[str, Any]] = []
    for market in market_list:
        market_data = redis_client.get(market)
        if market_data:
            result.append(json.loads(market_data))
        else:
            result.append({market: "No data found"})
    return JSONResponse(content=result)
