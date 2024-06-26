# api/exchange/trade.py
# API routers for cryptocurrency trading (buy, sell, etc)
# These API routers should be protected by authentication

from typing import Union
import json
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas import BuyCryptoSchema, SellCryptoSchema
from api.exchange.market import get_cryptocurrency_ticker

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from database_session import get_sqlite3_db
from ..user.authentication import get_current_user
from ..user.credentials import get_user_id_by_username
from models import User, Balance, TradeHistory, Statistics
from database_session import get_redis_db

# Get the current price of the cryptocurrency from the original data source
# Use price data from this so that the service is protected from the client request manipulation
async def get_current_crypto_price(market_code: str, redis_client) -> Union[None, float]:
    if not market_code:
        return None
    
    # Get the current price of the cryptocurrency from the Redis cache
    market_data = await get_cryptocurrency_ticker(markets=market_code, redis_client=redis_client)
    if not market_data:
        return None
    
    # Convert JSONResponse to JSON
    market_data = json.loads(market_data.body)

    return float(market_data[0]["trade_price"])

router: APIRouter = APIRouter()

# Buy cryptocurrency (not leverage trading)
@router.post("/api/exchange/trade/buy")
async def buy_crypto(
    request: BuyCryptoSchema,
    db: Session = Depends(get_sqlite3_db),
    redis_client = Depends(get_redis_db),
    current_user: User = Depends(get_current_user)
) -> JSONResponse:
    try:
        current_price: float = await get_current_crypto_price(f"KRW-{request.market_code}", redis_client)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Failed to get the current price of the cryptocurrency: {str(exception)}")

    # Get the user's balance
    username: str = current_user["username"]
    user_id: int = get_user_id_by_username(username, db)
    user_balance: Balance = db.query(Balance).filter(Balance.user_id == user_id).first()
    if not user_balance:
        raise HTTPException(status_code=404, detail="User balance not found")

    # Calculate the price information
    fee_rate: float = 0.0005 # 0.05% fee
    total_buy_price: float = current_price * request.amount * (1 + fee_rate)
    if user_balance.KRW < total_buy_price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    crypto_amount_attr = request.market_code
    crypto_avg_price_attr = f"{request.market_code}_average_unit_price"

    current_num_assets = getattr(user_balance, crypto_amount_attr, 0)
    current_avg_price = getattr(user_balance, crypto_avg_price_attr, 0)

    # Calculate new number of assets and new average price
    # (Calculating the entry price considering the average price of the existing assets)
    new_num_assets = current_num_assets + request.amount
    new_avg_price = ((current_avg_price * current_num_assets) + (current_price * request.amount)) / new_num_assets

    # Update the user's balance
    # (The value will be applied to the database)
    user_balance.KRW -= total_buy_price
    setattr(user_balance, crypto_amount_attr, new_num_assets)
    setattr(user_balance, crypto_avg_price_attr, new_avg_price)

    db.commit()
    db.refresh(user_balance)

    # Verify the updated balance; if any numerical value is negative, immediately reject the transaction
    if request.amount < 0 or current_price < 0 or user_balance.KRW < 0 or new_num_assets < 0 or new_avg_price < 0:
        raise HTTPException(status_code=400, detail="Invalid numeric value for buying cryptocurrency :P")

    # Save the trade history
    new_trade_history = TradeHistory(user_id=user_id,
                                     currency=request.market_code,
                                     amount=request.amount,
                                     price=current_price,
                                     transaction_type="buy",
                                     leverage_ratio=1)
    db.add(new_trade_history)
    db.commit()

    # Add the total transaction amount to the statistics
    # (The value will be applied to the database)
    statistics = db.query(Statistics).first()
    if not statistics:
        statistics = Statistics(total_transaction_amount=total_buy_price)
        db.add(statistics)
    else:
        statistics.total_transaction_amount += total_buy_price
    db.commit()

    # Return the response with data
    response_data: dict = {
        "message": "Successfully bought the cryptocurrency",
        "currency": request.market_code,
        "amount": request.amount,
        "price": current_price,
        "total_price": total_buy_price,
        "fee_rate": fee_rate,
        "fee": total_buy_price * fee_rate
    }
    return JSONResponse(content=response_data, status_code=200)

# Sell cryptocurrency (not leverage trading)
@router.post("/api/exchange/trade/sell")
async def sell_crypto(
    request: SellCryptoSchema,
    db: Session = Depends(get_sqlite3_db),
    redis_client = Depends(get_redis_db),
    current_user: User = Depends(get_current_user)
) -> JSONResponse:
    try:
        current_price: float = await get_current_crypto_price(f"KRW-{request.market_code}", redis_client)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Failed to get the current price of the cryptocurrency: {str(exception)}")

    # Get the user's balance
    username: str = current_user["username"]
    user_id: int = get_user_id_by_username(username, db)
    user_balance: Balance = db.query(Balance).filter(Balance.user_id == user_id).first()
    if not user_balance:
        raise HTTPException(status_code=404, detail="User balance not found")

    # Calculate the price information
    fee_rate: float = 0.0005

    # Check if the user has enough cryptocurrency to sell
    crypto_amount_attr = request.market_code
    if getattr(user_balance, crypto_amount_attr, 0) < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient cryptocurrency amount")
    
    # Update the user's balance
    total_sell_price: float = current_price * request.amount * (1 - fee_rate)
    user_balance.KRW += total_sell_price
    setattr(user_balance, crypto_amount_attr, getattr(user_balance, crypto_amount_attr, 0) - request.amount)
    db.commit()
    db.refresh(user_balance)

    # Verify the updated balance; if any numerical value is negative, immediately reject the transaction
    if request.amount < 0 or current_price < 0 or user_balance.KRW < 0 or getattr(user_balance, crypto_amount_attr, 0) < 0:
        raise HTTPException(status_code=400, detail="Invalid numeric value for selling cryptocurrency :P")

    # If the user has no more assets, reset the average price to 0
    if getattr(user_balance, crypto_amount_attr, 0) == 0:
        setattr(user_balance, f"{request.market_code}_average_unit_price", 0)
        db.commit()

    # Save the trade history
    new_trade_history = TradeHistory(user_id=user_id,
                                     currency=request.market_code,
                                     amount=request.amount,
                                     price=current_price,
                                     transaction_type="sell",
                                     leverage_ratio=1)
    db.add(new_trade_history)
    db.commit()

    # Add the total transaction amount to the statistics
    statistics = db.query(Statistics).first()
    if not statistics:
        statistics = Statistics(total_transaction_amount=total_sell_price)
        db.add(statistics)
    else:
        statistics.total_transaction_amount += total_sell_price

    # Return the response with data
    response_data: dict = {
        "message": "Successfully sold the cryptocurrency",
        "currency": request.market_code,
        "amount": request.amount,
        "price": current_price,
        "total_price": total_sell_price,
        "fee_rate": fee_rate,
        "fee": total_sell_price * fee_rate
    }
    return JSONResponse(content=response_data, status_code=200)
