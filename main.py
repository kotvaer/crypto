import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import ccxt
import os

# --- 配置 ---
EXCHANGE_ID = 'binance'
# SYMBOL = 'BTC/USDT'  # BTC 对 USDT 的交易对
SYMBOL = 'ETH/USDT'  # BTC 对 USDT 的交易对
INTERVAL_SECONDS = 0.5  # 每隔 5 秒获取一次价格

# --- 获取代理设置 (可以从环境变量获取) ---
# 注意：环境变量名通常是大写，无需 .lower()
http_proxy_env = os.environ.get('HTTP_PROXY'.lower())
https_proxy_env = os.environ.get('HTTPS_PROXY'.lower())
all_proxy_env = os.environ.get('ALL_PROXY'.lower())  # 有些系统或应用会用 ALL_PROXY

# 优先使用环境变量，如果环境变量未设置，则使用硬编码的代理
proxy_url = None
if all_proxy_env:
    proxy_url = all_proxy_env
elif http_proxy_env:
    proxy_url = http_proxy_env
elif https_proxy_env:
    proxy_url = https_proxy_env
else:
    # 默认 fallback 到你测试成功的 socks5 代理
    # 注意：这里修正了 http:// 前面多余的空格
    proxy_url = 'http://127.0.0.1:12334'

# 构建 ccxt 所需的 proxies 字典
proxy_settings = {}
if proxy_url:
    # ccxt 内部会解析 'socks5://' 或 'http://' 前缀
    proxy_settings = {
        'http': proxy_url,
        'https': proxy_url,
    }

# --- 初始化交易所 (只进行这一次初始化，确保带代理) ---
try:
    exchange = getattr(ccxt, EXCHANGE_ID)({
        'proxies': proxy_settings
    })
    print(f"Using proxy settings: {proxy_settings.get('http', 'None provided')}")

    # 删除了 exchange.fetch_exchange_info() 这一行，因为它不适用于 Binance
    print("Binance exchange initialized with proxy settings.")

except AttributeError:
    # 这个错误通常是 EXCHANGE_ID 拼写错误或 ccxt 版本过旧导致
    print(f"Error: Exchange '{EXCHANGE_ID}' not found. Please check the exchange ID or update ccxt library.")
    exit()
except Exception as e:  # 捕获更广泛的异常，包括网络和交易所错误
    print(f"An unexpected error occurred during exchange initialization: {e}")
    # 打印更多调试信息，比如代理设置是什么
    print(f"Proxy settings attempted: {proxy_settings}")
    exit()

# --- 数据存储 ---
prices = []
timestamps = []

# --- 绘图初始化 ---
fig, ax = plt.subplots()
line, = ax.plot([], [], label=f'{SYMBOL} Price')
ax.set_title(f'Real-time {SYMBOL} Price on {EXCHANGE_ID}')
ax.set_xlabel('Time')
ax.set_ylabel('Price (USDT)')
ax.grid(True)
ax.legend()


# --- 更新函数 (用于实时更新图表) ---
def update_price(frame):
    try:
        # 获取最新价格 (ticker 包含最新交易信息)
        ticker = exchange.fetch_ticker(SYMBOL)  # 这一行是主要的网络请求
        current_price = ticker['last']
        current_time = datetime.datetime.now()

        prices.append(current_price)
        timestamps.append(current_time)

        # 限制显示的数据点数量，避免图表过于拥挤
        max_data_points = 60  # 比如显示最近 5 分钟的数据 (60 * 5秒 = 300秒)
        if len(prices) > max_data_points:
            prices.pop(0)
            timestamps.pop(0)

        # 更新图表数据
        line.set_data(timestamps, prices)

        # 自动调整X轴和Y轴范围
        ax.relim()
        ax.autoscale_view()

        # 格式化X轴时间显示
        fig.autofmt_xdate()

        print(f"{current_time.strftime('%H:%M:%S')} - {SYMBOL} Price: {current_price}")

    except ccxt.NetworkError as e:
        print(f"Network error: {e}. Retrying...")
    except ccxt.ExchangeError as e:
        print(f"Exchange error: {e}. Please check the symbol or exchange status.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- 启动实时更新 ---
# FuncAnimation 会重复调用 update_price 函数，interval 参数以毫秒为单位
ani = animation.FuncAnimation(fig, update_price, interval=INTERVAL_SECONDS * 1000)

plt.show()