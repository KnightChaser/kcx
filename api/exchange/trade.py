# api/exchange/trade.py
# API routers for cryptocurrency trading (buy, sell, etc)
# These API routers should be protected by authentication

from typing import Union
import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas import BuyCryptoSchema, SellCryptoSchema, TradeHistorySchema

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from database_session import get_db
from ..user.authentication import get_current_user
from ..user.credentials import get_user_id_by_username
from models import User, Balance, TradeHistory

# Get the current price of the cryptocurrency from the original data source
# Use price data from this so that the service is protected from the client request manipulation
def get_current_crypto_price(market_code: str) -> Union[None, float]:
    if not market_code:
        return None
    
    # Get the current price of the cryptocurrency
    api_url: str = f"https://api.upbit.com/v1/ticker?markets=KRW-{market_code}"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to get the current price of the cryptocurrency(bad status code {response.status_code}), url {api_url}")

    response_json = response.json()
    if not response_json:
        raise Exception(f"Failed to get the current price of the cryptocurrency(failed to convert the response into JSON), url {api_url}")

    return float(response_json[0]["trade_price"])

router: APIRouter = APIRouter()

# Buy cryptocurrency (not leverage trading)
@router.post("/exchange/trade/buy")
def buy_crypto(request: BuyCryptoSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> JSONResponse:
    try:
        current_price: float = get_current_crypto_price(request.market_code)
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

    # Update the user's balance
    user_balance.KRW -= total_buy_price
    crypto_amount_attr = request.market_code
    crypto_avg_price_attr = f"{request.market_code}_average_unit_price"

    # Update cryptocurrency amount
    setattr(user_balance, crypto_amount_attr, getattr(user_balance, crypto_amount_attr, 0) + request.amount)

    # Update average unit price of the cryptocurrency asset that the target user has
    current_num_assets = getattr(user_balance, crypto_amount_attr, 0)
    current_avg_price = getattr(user_balance, crypto_avg_price_attr, 0)

    new_avg_price = ((current_avg_price * current_num_assets) + (current_price * request.amount)) / (current_num_assets + request.amount)
    setattr(user_balance, crypto_avg_price_attr, new_avg_price)

    db.commit()
    db.refresh(user_balance)

    # Save the trade history
    new_trade_history = TradeHistory(user_id=user_id,
                                     currency=request.market_code,
                                     amount=request.amount,
                                     price=current_price,
                                     transaction_type="buy",
                                     leverage_ratio=1)
    db.add(new_trade_history)
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
@router.post("/exchange/trade/sell")
def sell_crypto(request: SellCryptoSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> JSONResponse:
    try:
        current_price: float = get_current_crypto_price(request.market_code)
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

    # Save the trade history
    new_trade_history = TradeHistory(user_id=user_id,
                                     currency=request.market_code,
                                     amount=request.amount,
                                     price=current_price,
                                     transaction_type="sell",
                                     leverage_ratio=1)
    db.add(new_trade_history)
    db.commit()

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