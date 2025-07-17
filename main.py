import datetime
import ccxt
import os
import time
import plotly.graph_objects as go

# --- 配置 ---
EXCHANGE_ID = 'binance'
SYMBOL = 'ETH/USDT'
INTERVAL_SECONDS = 0.5

# --- 获取代理设置 ---
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
    proxy_url = 'http://127.0.0.1:12334'

proxy_settings = {}
if proxy_url:
    proxy_settings = {
        'http': proxy_url,
        'https': proxy_url,
    }

# --- 初始化交易所 ---
try:
    exchange = getattr(ccxt, EXCHANGE_ID)({
        'proxies': proxy_settings
    })
    print(f"Using proxy settings: {proxy_settings.get('http', 'None provided')}")
    print("Binance exchange initialized with proxy settings.")

except AttributeError:
    print(f"Error: Exchange '{EXCHANGE_ID}' not found. Please check the exchange ID or update ccxt library.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred during exchange initialization: {e}")
    print(f"Proxy settings attempted: {proxy_settings}")
    exit()

# --- 数据存储 ---
prices = []
timestamps = []

# --- Plotly 图表初始化 ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=f'{SYMBOL} Price'))
fig.update_layout(
    title=f'Real-time {SYMBOL} Price on {EXCHANGE_ID}',
    xaxis_title='Time',
    yaxis_title='Price (USDT)',
    hovermode='x unified' # 统一显示X轴上的所有数据点信息
)

# --- 主循环，实时更新数据并保存图表 ---
print("Starting real-time price updates. Open 'realtime_price_chart.html' in your browser and refresh manually to see updates.")

while True:
    try:
        ticker = exchange.fetch_ticker(SYMBOL)
        current_price = ticker['last']
        current_time = datetime.datetime.now()

        prices.append(current_price)
        timestamps.append(current_time)

        # 限制显示的数据点数量
        max_data_points = 120  # 比如显示最近 1 分钟的数据 (120 * 0.5秒 = 60秒)
        if len(prices) > max_data_points:
            prices.pop(0)
            timestamps.pop(0)

        # 更新 Plotly 图表数据
        with fig.batch_update():
            fig.data[0].x = timestamps
            fig.data[0].y = prices

        # 保存为 HTML 文件
        fig.write_html("realtime_price_chart.html")

        print(f"{current_time.strftime('%H:%M:%S')} - {SYMBOL} Price: {current_price}")

    except ccxt.NetworkError as e:
        print(f"Network error: {e}. Retrying...")
    except ccxt.ExchangeError as e:
        print(f"Exchange error: {e}. Please check the symbol or exchange status.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    time.sleep(INTERVAL_SECONDS)
