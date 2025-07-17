import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from collections import deque
import random
import datetime

# 如果ccxt连接正常，你可以在这里初始化交易所
# import ccxt
# exchange = ccxt.binance()

X = deque(maxlen=20)
X.append(datetime.datetime.now())
Y = deque(maxlen=20)
Y.append(100)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=5 * 1000,  # 每5秒更新一次
            n_intervals=0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    # 模拟数据更新
    # 如果ccxt连接正常，你可以在这里获取实时数据
    # try:
    #     ticker = exchange.fetch_ticker('BTC/USDT')
    #     current_price = ticker['last']
    # except Exception as e:
    #     print(f"Error fetching data: {e}")
    #     current_price = Y[-1] # 使用上一个价格作为备用

    X.append(datetime.datetime.now())
    Y.append(Y[-1] + Y[-1] * random.uniform(-0.01, 0.01)) # 模拟价格波动

    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                yaxis=dict(range=[min(Y), max(Y)]),
                                title='实时价格图表 (模拟数据)'
                                )}

if __name__ == '__main__':
    app.run(debug=True)
