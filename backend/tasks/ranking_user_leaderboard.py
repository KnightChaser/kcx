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
from rich.console import Console
from typing import List, Dict

import sys
sys.path.append("..")
from database_session import get_sqlite3_db, get_redis_db
from models import User, Balance

def rank_user_leaderboard(update_interval_in_seconds: int) -> None:
    console: Console = Console()
    iteration_count: int = 0

    while True:
        try:
            # Create a new SQLite session for this iteration
            with next(get_sqlite3_db()) as sqlite3_db:
                redis_db = get_redis_db()

                # Get the users and their balances from the SQLite3 database
                users: List[User] = sqlite3_db.query(User).all()
                user_balances: Dict[int, Balance] = {balance.user_id: balance for balance in sqlite3_db.query(Balance).all()}

                user_total_assets = {}

                # Fetch all available cryptocurrency types and current prices
                all_crypto_assets = [col for col in Balance.__table__.columns.keys() if col not in {"id", "user_id", "created_at", "KRW"} and not col.endswith("_average_unit_price")]
                crypto_prices = {crypto: json.loads(redis_db.get(f"KRW-{crypto}"))["trade_price"] for crypto in all_crypto_assets}

                # Calculate the user's total asset value
                for user in users:
                    balance = user_balances.get(user.id)
                    if balance:
                        total_asset_value = balance.KRW  # Start with KRW balance
                        for crypto in all_crypto_assets:
                            crypto_balance = getattr(balance, crypto, 0)
                            current_price = crypto_prices.get(crypto, 0)
                            total_asset_value += crypto_balance * current_price

                        user_total_assets[user.id] = total_asset_value

                # Associate the user's name with their total asset value
                user_total_assets_with_name = {user.username: user_total_assets[user.id] for user in users if user.id in user_total_assets}

                # Sort the user's total asset value in descending order
                sorted_user_total_assets = dict(sorted(user_total_assets_with_name.items(), key=lambda item: item[1], reverse=True))

                # Store the user's ranking in the Redis database
                redis_db.set("user_leaderboard", json.dumps(sorted_user_total_assets))

                iteration_count += 1
                console.log(f"user leaderboard calculated (cycle: {iteration_count})")
                time.sleep(update_interval_in_seconds)
        except Exception as e:
            console.log(f"Exception in rank_user_leaderboard: {e}")
            time.sleep(1)  # Brief pause before restarting

# Start the task in a separate thread
# In case of an exception and cessation of the task, it will be restarted after 1 second
def start_rank_user_leaderboard(update_interval_in_seconds: int) -> None:
    def run_with_restart():
        console: Console = Console()
        while True:
            try:
                rank_user_leaderboard(update_interval_in_seconds)
            except Exception as e:
                console.log(f"Exception in task rank_user_leaderboard: {e}, restarting in 1 second")
                time.sleep(1)  # Brief pause before restarting

    thread = threading.Thread(target=run_with_restart)
    thread.daemon = True
    thread.start()
