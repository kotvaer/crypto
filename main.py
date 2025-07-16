import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time


def fetch_btc_historical_prices(exchange='binance', timeframe='1d', days=7):
    # Initialize the exchange
    exchange_obj = getattr(ccxt, exchange)()

    # Calculate the start time
    since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)

    # Fetch OHLCV (Open, High, Low, Close, Volume) data
    ohlcv = exchange_obj.fetch_ohlcv('BTC/USDT', timeframe, since)

    # Create DataFrame
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # Convert timestamp to readable date
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')

    # Select and rename relevant columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df.columns = ['Date', 'Open ($)', 'High ($)', 'Low ($)', 'Close ($)', 'Volume (BTC)']

    # Round price columns to 2 decimal places
    price_columns = ['Open ($)', 'High ($)', 'Low ($)', 'Close ($)']
    df[price_columns] = df[price_columns].round(2)

    # Format Volume to 2 decimal places
    df['Volume (BTC)'] = df['Volume (BTC)'].round(2)

    # Set Date as index
    df.set_index('Date', inplace=True)

    return df


def display_btc_price_table(days=7):
    try:
        # Fetch the data
        df = fetch_btc_historical_prices(days=days)

        # Display the table
        print(f"\nBTC/USDT Historical Prices (Last {days} Days)")
        print("=" * 50)
        print(df.to_string())
        print("=" * 50)

    except Exception as e:
        print(f"Error fetching data: {str(e)}")


if __name__ == "__main__":
    # Example usage: Default (7 days)
    display_btc_price_table()

    # Example with custom days (e.g., 30 days)
    # display_btc_price_table(days=30)