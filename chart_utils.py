# chart_utils.py

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

def create_candlestick_chart(ohlcv_data, symbol):
    if not ohlcv_data:
        return go.Figure()

    df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, 
                        row_heights=[0.7, 0.3]) # K线图占70%，成交量占30%

    # K线图
    fig.add_trace(go.Candlestick(x=df['timestamp'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='Candlestick'), row=1, col=1)

    # 成交量图
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['volume'], name='Volume',
                         marker_color='rgba(0,150,136,0.5)'), row=2, col=1) # 绿色

    fig.update_layout(
        title=f'{symbol} K线图',
        xaxis_rangeslider_visible=False, # 隐藏底部时间滑块
        hovermode='x unified',
        height=700 # 调整图表高度
    )

    fig.update_yaxes(title_text="价格", row=1, col=1)
    fig.update_yaxes(title_text="成交量", row=2, col=1)

    return fig
