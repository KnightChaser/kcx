# api/exchange/market.py
# API routers for cryptocurrency market data (public)
# These API routers should be open to the public, no authentication required

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from models import Balance

router:APIRouter = APIRouter()

# Get the currently supported cryptocurrency list by this exchange
@router.get("/exchange/market/list")
def get_cryptocurrency_list():
    # Available cryptocurrency lists are in the Balance model
    cryptocurrency_list = Balance.__table__.columns.keys()

    # Except for the
    # - id
    # - user_id
    # - created_at
    # - KRW (fiat currency)
    cryptocurrency_list.remove("id")
    cryptocurrency_list.remove("user_id")
    cryptocurrency_list.remove("created_at")
    cryptocurrency_list.remove("KRW")

    return JSONResponse(content=cryptocurrency_list)