# tasks/fetch_and_store_market_data.py
# Fetch the crypto market data from UpBIT API and store it in the Redis database to resolve the API quota issue.

import requests
import redis
import json
import threading
import time
from rich.console import Console

# Note that these packages are in the parent directory
import sys
sys.path.append("..")
from api.exchange.market import get_cryptocurrency_list


# Store the market data in the Redis database periodically
def fetch_and_store_market_data(redis_host:str, redis_port: int, database: int, update_interval_in_seconds: int) -> None:
    console:Console = Console()
    request_count:int = 0

    # Convert market list to string such as ["ADA", "BTC", "ETH"] to "KRW-ADA,KRW-BTC,KRW-ETH" (hyphen, comma, and "KRW" prefix)
    market_code_request_list:str = json.loads(get_cryptocurrency_list().body)
    market_code_request_string:str = ""
    for market_code in market_code_request_list:
        market_code_request_string += f"KRW-{market_code},"
    market_code_request_string = market_code_request_string[:-1]        # Remove the last comma

    url:str = f"https://api.upbit.com/v1/ticker?markets={market_code_request_string}"
    redis_client = redis.Redis(host=redis_host, 
                               port=redis_port, 
                               db=database)
    console.log(f"Connected to Redis database at {redis_host}:{redis_port}/{database}")
    console.log(f"Requesting to {url} to gather cryptocurrency market data (cycle: {request_count})")

    while True:
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
        # Fetch and store the market data every second
        time.sleep(update_interval_in_seconds)

def start_fetch_and_store_market_data(redis_host:str, redis_port: int, database: int, update_interval_in_seconds: int) -> None:
    thread = threading.Thread(target=fetch_and_store_market_data, args=(redis_host, redis_port, database, update_interval_in_seconds))
    thread.daemon = True
    thread.start()