# data_fetcher.py

import ccxt
import os
from config import EXCHANGE_ID, PROXY_DEFAULT_URL, OHLCV_TIMEFRAME, OHLCV_LIMIT

exchange = None

def get_proxy_settings():
    http_proxy_env = os.environ.get('HTTP_PROXY'.lower())
    https_proxy_env = os.environ.get('HTTPS_PROXY'.lower())
    all_proxy_env = os.environ.get('ALL_PROXY'.lower())

    proxy_url = None
    if all_proxy_env:
        proxy_url = all_proxy_env
    elif http_proxy_env:
        proxy_url = http_proxy_env
    elif https_proxy_env:
        proxy_url = https_proxy_env
    else:
        proxy_url = PROXY_DEFAULT_URL

    proxy_settings = {}
    if proxy_url:
        proxy_settings = {
            'http': proxy_url,
            'https': proxy_url,
        }
    return proxy_settings

def initialize_exchange():
    global exchange
    if exchange is None:
        proxy_settings = get_proxy_settings()
        try:
            exchange = getattr(ccxt, EXCHANGE_ID)({
                'proxies': proxy_settings
            })
            print(f"Using proxy settings: {proxy_settings.get('http', 'None provided')}")
            print(f"{EXCHANGE_ID} exchange initialized with proxy settings.")
        except AttributeError:
            print(f"Error: Exchange '{EXCHANGE_ID}' not found. Please check the exchange ID or update ccxt library.")
            exchange = None
        except Exception as e:
            print(f"An unexpected error occurred during exchange initialization: {e}")
            exchange = None
    return exchange

def fetch_ohlcv(symbol):
    exchange = initialize_exchange()
    if exchange is None:
        return None
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, OHLCV_TIMEFRAME, limit=OHLCV_LIMIT)
        return ohlcv
    except ccxt.NetworkError as e:
        print(f"Network error fetching OHLCV for {symbol}: {e}. Retrying...")
        return None
    except ccxt.ExchangeError as e:
        print(f"Exchange error fetching OHLCV for {symbol}: {e}. Please check the symbol or exchange status.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred fetching OHLCV for {symbol}: {e}")
        return None

def fetch_ticker(symbol):
    exchange = initialize_exchange()
    if exchange is None:
        return None
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker
    except ccxt.NetworkError as e:
        print(f"Network error fetching ticker for {symbol}: {e}. Retrying...")
        return None
    except ccxt.ExchangeError as e:
        print(f"Exchange error fetching ticker for {symbol}: {e}. Please check the symbol or exchange status.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred fetching ticker for {symbol}: {e}")
        return None
