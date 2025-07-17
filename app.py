import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go

from data_fetcher import fetch_ohlcv, fetch_ticker, initialize_exchange
from chart_utils import create_candlestick_chart
from config import DEFAULT_SYMBOL, UPDATE_INTERVAL_MS, EXCHANGE_ID

app = dash.Dash(__name__)

# 初始化交易所一次
initialize_exchange()

app.layout = html.Div(
    [
        html.H1(f'{EXCHANGE_ID} 实时交易数据'),
        html.Div([
            html.Label('选择交易对:'),
            dcc.Input(
                id='symbol-input',
                type='text',
                value=DEFAULT_SYMBOL,
                debounce=True, # 用户输入完成后才触发更新
                style={'marginRight': '10px'}
            ),
            html.Div(id='live-price-display', style={'display': 'inline-block', 'marginLeft': '20px', 'fontWeight': 'bold'})
        ]),
        dcc.Graph(id='live-candlestick-graph', animate=False), # K线图不使用animate，因为数据量大
        dcc.Interval(
            id='graph-update',
            interval=UPDATE_INTERVAL_MS,
            n_intervals=0
        ),
    ]
)

# 回调函数：更新K线图和实时价格
@app.callback(
    [Output('live-candlestick-graph', 'figure'),
     Output('live-price-display', 'children')],
    [Input('graph-update', 'n_intervals'),
     Input('symbol-input', 'value')]
)
def update_graph_and_price(n, selected_symbol):
    # 获取OHLCV数据
    ohlcv_data = fetch_ohlcv(selected_symbol.upper())
    fig = create_candlestick_chart(ohlcv_data, selected_symbol.upper())

    # 获取实时价格
    ticker_data = fetch_ticker(selected_symbol.upper())
    live_price_text = "获取价格失败"
    if ticker_data and 'last' in ticker_data:
        live_price_text = f'最新价格: {ticker_data['last']:.2f}'

    return fig, live_price_text

if __name__ == '__main__':
    app.run(debug=True)
