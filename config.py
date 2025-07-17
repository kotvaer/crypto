# config.py

EXCHANGE_ID = 'binance'
DEFAULT_SYMBOL = 'ETH/USDT'
UPDATE_INTERVAL_MS = 0.5 * 1000  # 0.5秒更新一次
OHLCV_TIMEFRAME = '1m' # 默认1分钟K线
OHLCV_LIMIT = 100 # 获取最近100根K线

# 默认代理地址，如果环境变量中没有设置
PROXY_DEFAULT_URL = 'http://127.0.0.1:12334'

# 可供选择的交易对
AVAILABLE_SYMBOLS = [
    'BTC/USDT',
    'ETH/USDT',
    'BNB/USDT',
    'XRP/USDT',
    'DOGE/USDT',
]

# 可供选择的K线周期
AVAILABLE_TIMEFRAMES = [
    '1m',   # 1分钟
    '5m',   # 5分钟
    '15m',  # 15分钟
    '30m',  # 30分钟
    '1h',   # 1小时
    '4h',   # 4小时
    '1d',   # 1天
    '1w',   # 1周
    '1M',   # 1月
]
