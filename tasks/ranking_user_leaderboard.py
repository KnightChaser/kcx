# tasks/ranking_user_leaderboard.py
# Tasks
# 1. Periodically track the user's balances from the database(SQLite3)
# 2. Calculate the user's total asset value by considering the current market price(Redis)
# 3. Rank the users based on their total asset value
# 4. Store the user's ranking in the Redis database
# 5. Periodically update the user's ranking (e.g. every 1 minute)
# (Note that the API endpoint will be served on /backend/api/statistics/statistics.py)

import threading
import time
import json
from sqlalchemy.orm import Session
from rich.console import Console
from typing import List

# Note that these packages are in the parent directory
import sys
sys.path.append("..")
from database_session import get_sqlite3_db, get_redis_db
from models import User, Balance

def rank_user_leaderboard(update_interval_in_seconds: int) -> None:
    console: Console = Console()
    iteration_count: int = 0

    while True:
        # Create a new SQLite session for this thread
        sqlite3_db: Session = next(get_sqlite3_db())
        redis_db = get_redis_db()

        # Get the user's balances from the SQLite3 database
        users: List[User] = sqlite3_db.query(User).all()
        user_balances: List[Balance] = sqlite3_db.query(Balance).all()

        user_total_assets = {user.id: user_balance.KRW for user, user_balance in zip(users, user_balances)}

        # Calculate the user's total asset value by considering the current market price(Redis)
        # (user's total asset value) = (user's KRW balance) + (user's BTC balance) * (current BTC price) + ... (for all currencies)
        for user in users:
            for user_balance_data_row in user_balances:
                # Get all available cryptocurrency types
                availble_crypto_asset_type: List[str] = user_balance_data_row.__table__.columns.keys()
                availble_crypto_asset_type.remove("id")
                availble_crypto_asset_type.remove("user_id")
                availble_crypto_asset_type.remove("created_at")
                availble_crypto_asset_type.remove("KRW")
                for column in user_balance_data_row.__table__.columns.keys():
                    if column.endswith("_average_unit_price"):
                        availble_crypto_asset_type.remove(column)

                # Calculate the user's total asset value
                for crypto_asset_type in availble_crypto_asset_type:
                    current_crypto_price = redis_db.get(f"KRW-{crypto_asset_type}")
                    current_crypto_price = json.loads(current_crypto_price)["trade_price"]
                    user_total_assets[user.id] += user_balance_data_row.__getattribute__(crypto_asset_type) * current_crypto_price

        # Now we have the user's total asset value in the user_total_assets dictionary
        # i.e. {1: 1000000, 2: 2000000, ...}

        # Associate the user's name with the sorted_user_total_assets's key(user ID)
        user_total_assets_with_name = {}
        for user in users:
            user_total_assets_with_name[user.username] = user_total_assets[user.id]

        # Sort the user's total asset value in descending order
        sorted_user_total_assets = dict(sorted(user_total_assets_with_name.items(), key=lambda item: item[1], reverse=True))

        # Store the user's ranking in the Redis database
        redis_db.set("user_leaderboard", json.dumps(sorted_user_total_assets))

        iteration_count += 1
        console.log(f"user leaderboard calculated (cycle: {iteration_count})")
        time.sleep(update_interval_in_seconds)

def start_rank_user_leaderboard(update_interval_in_seconds: int) -> None:
    thread = threading.Thread(target=rank_user_leaderboard, args=(update_interval_in_seconds,))
    thread.daemon = True
    thread.start()
