# tasks/fetch_and_store_market_data.py
# Fetch the crypto market data from UpBIT API and store it in the Redis database to resolve the API quota issue.

import requests
import json
import threading
import time
from rich.console import Console

# Note that these packages are in the parent directory
import sys
sys.path.append("..")
from api.exchange.market import get_cryptocurrency_list

def fetch_and_store_market_data(redis_client, update_interval_in_seconds: int) -> None:
    console: Console = Console()
    request_count: int = 0

    market_code_request_list: str = json.loads(get_cryptocurrency_list().body)
    market_code_request_string: str = ""
    for market_code in market_code_request_list:
        market_code_request_string += f"KRW-{market_code},"
    market_code_request_string = market_code_request_string[:-1]  # Remove the last comma

    url: str = f"https://api.upbit.com/v1/ticker?markets={market_code_request_string}"
    console.log(f"Connected to Redis database")
    console.log(f"Requesting to {url} to gather cryptocurrency market data (cycle: {request_count})")

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    market_code = item['market']
                    market_data = json.dumps(item)
                    redis_client.set(market_code, market_data)
                request_count += 1
                console.log(f"Successfully stored the market data from UpBIT API in the Redis database (cycle: {request_count})")
            else:
                console.log(f"Failed to request to {url} (status code: {response.status_code})")
            time.sleep(update_interval_in_seconds)
        except Exception as e:
            console.log(f"Exception in fetch_and_store_market_data: {e}")
            time.sleep(1)  # Brief pause before restarting

# Start the task in a separate thread
# In case of an exception ceasation of the task, it will be restarted after 1 second
def start_fetch_and_store_market_data(redis_client, update_interval_in_seconds: int) -> None:
    def run_with_restart():
        console: Console = Console()
        while True:
            try:
                fetch_and_store_market_data(redis_client, update_interval_in_seconds)
            except Exception as e:
                console.log(f"Exception in task fetch_and_store_market_data: {e}, restarting in 1 second")
                time.sleep(1)  # Brief pause before restarting

    thread = threading.Thread(target=run_with_restart)
    thread.daemon = True
    thread.start()
