import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc # 导入dash_bootstrap_components

from data_fetcher import fetch_ohlcv, fetch_ticker, initialize_exchange
from chart_utils import create_candlestick_chart
from config import DEFAULT_SYMBOL, UPDATE_INTERVAL_MS, EXCHANGE_ID, AVAILABLE_SYMBOLS, AVAILABLE_TIMEFRAMES, OHLCV_TIMEFRAME

# 使用一个暗色主题
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# 初始化交易所一次
initialize_exchange()

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1(f'{EXCHANGE_ID} 实时交易数据', className="text-center my-4"), width=12)
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label('选择交易对:', className="me-2"),
                                dcc.Dropdown(
                                    id='symbol-dropdown',
                                    options=[{'label': s, 'value': s} for s in AVAILABLE_SYMBOLS],
                                    value=DEFAULT_SYMBOL,
                                    clearable=False,
                                    className="mb-3", # 添加一些底部外边距
                                    style={'color': '#212529'} # 确保下拉框文字颜色在暗色主题下可见
                                ),
                                html.Label('选择K线周期:', className="me-2"),
                                dcc.Dropdown(
                                    id='timeframe-dropdown',
                                    options=[{'label': t, 'value': t} for t in AVAILABLE_TIMEFRAMES],
                                    value=OHLCV_TIMEFRAME,
                                    clearable=False,
                                    style={'color': '#212529'} # 确保下拉框文字颜色在暗色主题下可见
                                ),
                            ]
                        ),
                        className="mb-4", # 添加一些底部外边距
                    ),
                    md=4 # 在中等屏幕上占4列
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4('最新价格', className="card-title"),
                                html.Div(id='live-price-display', className="display-4 text-success") # 使用Bootstrap的显示类和颜色
                            ]
                        )
                    ),
                    md=8 # 在中等屏幕上占8列
                )
            ],
            className="mb-4" # 添加一些底部外边距
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='live-candlestick-graph', animate=False, config={'displayModeBar': False}), # 隐藏Plotly的工具栏
                width=12
            )
        ),
        dcc.Interval(
            id='graph-update',
            interval=UPDATE_INTERVAL_MS,
            n_intervals=0
        ),
    ],
    fluid=True, # 容器宽度占满整个屏幕
    className="bg-dark text-light" # 设置容器背景色和文字颜色
)

# 回调函数：更新K线图和实时价格
@app.callback(
    [Output('live-candlestick-graph', 'figure'),
     Output('live-price-display', 'children')],
    [Input('graph-update', 'n_intervals'),
     Input('symbol-dropdown', 'value'),
     Input('timeframe-dropdown', 'value')]
)
def update_graph_and_price(n, selected_symbol, selected_timeframe):
    # 获取OHLCV数据
    ohlcv_data = fetch_ohlcv(selected_symbol.upper(), selected_timeframe)
    fig = create_candlestick_chart(ohlcv_data, selected_symbol.upper())

    # 获取实时价格
    ticker_data = fetch_ticker(selected_symbol.upper())
    live_price_text = "获取价格失败"
    if ticker_data and 'last' in ticker_data:
        live_price_text = f'{ticker_data['last']:.2f}'

    return fig, live_price_text

if __name__ == '__main__':
    app.run(debug=True)
