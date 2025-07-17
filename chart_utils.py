# chart_utils.py

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

def create_candlestick_chart(ohlcv_data, symbol):
    if not ohlcv_data:
        # 返回一个空的图表，并设置背景色和字体颜色以适应暗色主题
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark", # 使用暗色主题模板
            title=f'{symbol} K线图',
            xaxis_title='时间',
            yaxis_title='价格',
            height=700,
            annotations=[
                dict(
                    text="无数据",
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=28, color="#cccccc")
                )
            ]
        )
        return fig

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
                                 name='Candlestick',
                                 increasing_line_color='#00CC96', # 绿色
                                 decreasing_line_color='#EF553B'), # 红色
                                 row=1, col=1)

    # 成交量图
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['volume'], name='Volume',
                         marker_color='#636EFA'), # 蓝色，与暗色主题更搭
                         row=2, col=1)

    fig.update_layout(
        template="plotly_dark", # 使用暗色主题模板
        title=f'{symbol} K线图',
        xaxis_rangeslider_visible=False, # 隐藏底部时间滑块
        hovermode='x unified',
        height=700 # 调整图表高度
    )

    fig.update_yaxes(title_text="价格", row=1, col=1)
    fig.update_yaxes(title_text="成交量", row=2, col=1)

    return fig