# config.py

EXCHANGE_ID = 'binance'
DEFAULT_SYMBOL = 'ETH/USDT'
UPDATE_INTERVAL_MS = 5 * 1000  # 5秒更新一次
OHLCV_TIMEFRAME = '1m' # 1分钟K线
OHLCV_LIMIT = 100 # 获取最近100根K线

# 默认代理地址，如果环境变量中没有设置
PROXY_DEFAULT_URL = 'http://127.0.0.1:12334'
