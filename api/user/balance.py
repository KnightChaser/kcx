# api/usuer/balance.py
# API routers for user balance management
# These API routers should be protected from unauthorized access

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import DepositWithdrawHistory, TradeHistory
from schemas import BalanceSchema, BalanceDepositWithdrawSchema
from .authentication import get_current_user
from .credentials import get_user_id_by_username

# Note that those packages are located in the parent directory
import sys
sys.path.append("..")
from models import User, Balance
from database_session import get_db

router:APIRouter = APIRouter()

# Get the user's balance
# We don't care how the balance model is implemented, just return the balance
# ex) {"KRW": 1000000, "BTC": 0.1, "ETH": 0.5, "XRP": 1000}
@router.get("/api/account/balance/")
def get_balance(db:Session = Depends(get_db), current_user:User = Depends(get_current_user)) -> BalanceSchema:
    username:str = current_user["username"]
    user_id:int = get_user_id_by_username(username, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    balance = db.query(Balance).filter(Balance.user_id == user_id).first()
    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found")
    return balance

# Deposit money(KRW; fiat currency) to the user's account
@router.post("/api/account/deposit/KRW", response_model=BalanceDepositWithdrawSchema)
def deposit_KRW(deposit_balance: BalanceDepositWithdrawSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> BalanceDepositWithdrawSchema:
    # Deposit can't be a negative number
    if deposit_balance.KRW <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deposit amount must be greater than zero")
    
    username: str = current_user["username"]
    user_id: int = get_user_id_by_username(username, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    account_balance = db.query(Balance).filter(Balance.user_id == user_id).first()
    if not account_balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found")
    
    account_balance.KRW += deposit_balance.KRW
    db.commit()
    db.refresh(account_balance)  # Refresh the ORM model instance

    # Create a new deposit history
    deposit_history = DepositWithdrawHistory(user_id=user_id, 
                                             currency="KRW", 
                                             amount=deposit_balance.KRW, 
                                             transaction_type="deposit")
    create_deposit_withdraw_history(deposit_history, db)

    return BalanceDepositWithdrawSchema(KRW=account_balance.KRW)

# Withdraw money(KRW; fiat currency) from the user's account
@router.post("/api/account/withdraw/KRW", response_model=BalanceDepositWithdrawSchema)
def withdraw_KRW(withdraw_balance: BalanceDepositWithdrawSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> BalanceDepositWithdrawSchema:
    # Withdraw can't be a negative number
    if withdraw_balance.KRW <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Withdraw amount must be greater than zero")
    
    username: str = current_user["username"]
    user_id: int = get_user_id_by_username(username, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    account_balance = db.query(Balance).filter(Balance.user_id == user_id).first()
    if not account_balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found")
    
    if account_balance.KRW < withdraw_balance.KRW:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
    
    account_balance.KRW -= withdraw_balance.KRW
    db.commit()
    db.refresh(account_balance)

    # Create a new withdraw history
    withdraw_history = DepositWithdrawHistory(user_id=user_id, 
                                              currency="KRW", 
                                              amount=withdraw_balance.KRW, 
                                              transaction_type="withdraw")
    create_deposit_withdraw_history(withdraw_history, db)

    return BalanceDepositWithdrawSchema(KRW=account_balance.KRW)

# Create a new balance deposit and withdraw history
def create_deposit_withdraw_history(DepositWithdrawHistory: DepositWithdrawHistory, db: Session):
    db.add(DepositWithdrawHistory)
    db.commit()
    db.refresh(DepositWithdrawHistory)

# Get the user's balance deposit and withdraw history
@router.get("/api/account/deposit_withdraw/history/")
def get_deposit_withdraw_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), length:int = 20):
    username: str = current_user["username"]
    user_id: int = get_user_id_by_username(username, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Get the user's deposit and withdraw history with the specified length, in descending order in terms of the creation time
    history = db.query(DepositWithdrawHistory).filter(DepositWithdrawHistory.user_id == user_id).order_by(DepositWithdrawHistory.created_at.desc()).limit(length).all()
    return history

# Get the user's crypto transaction history (buy/sell)
@router.get("/api/account/crypto_trade/history/")
def get_crypto_transaction_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), length:int = 50):
    username: str = current_user["username"]
    user_id: int = get_user_id_by_username(username, db)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Get the user's crypto transaction history with the specified length, in descending order in terms of the creation time
    history = db.query(TradeHistory).filter(TradeHistory.user_id == user_id).order_by(TradeHistory.created_at.desc()).limit(length).all()
    return history