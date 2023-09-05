import ccxt
import pandas as pd
import plotly.graph_objects as go

exchange = ccxt.binance(
    {
        "enableRateLimit": True,
    }
)

# Get the historical prices for a cryptocurrency
symbol = "BTC/USDT"
timeframe = "1h"
limit = 1000
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(
    ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

df = df[df["volume"] != 0]
df.reset_index(drop=True, inplace=True)
df.isna().sum()
df.tail()


def support(df1, l, n1, n2):  # n1 n2 before and after candle l
    for i in range(l - n1 + 1, l + 1):
        if df1.low[i] > df1.low[i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if df1.low[i] < df1.low[i - 1]:
            return 0
    return 1


def resistance(df1, l, n1, n2):  # n1 n2 before and after candle l
    for i in range(l - n1 + 1, l + 1):
        if df1.high[i] < df1.high[i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if df1.high[i] > df1.high[i - 1]:
            return 0
    return 1


ss = []
rr = []
n1 = 3
n2 = 3
for row in range(n1, len(df) - n2):  # len(df)-n2
    if support(df, row, n1, n2):
        ss.append((row, df.low[row]))
    if resistance(df, row, n1, n2):
        rr.append((row, df.high[row]))

# sorting support and resistance lines by price
ss.sort(key=lambda x: x[1])
rr.sort(key=lambda x: x[1])

# getting rid of support and resistance lines that are too close to each other

ss1 = []
rr1 = []
last_price = None
tolerance = 100
for timestamp, price in ss:
    if last_price is None or abs(price - last_price) > tolerance:
        ss1.append((timestamp, price))
        last_price = price
last_price = None
for timestamp, price in rr:
    if last_price is None or abs(price - last_price) > tolerance:
        rr1.append((timestamp, price))
        last_price = price
ss = ss1
rr = rr1


dfpl = df

fig = go.Figure(
    data=[
        go.Candlestick(
            x=dfpl.index,
            open=dfpl["open"],
            high=dfpl["high"],
            low=dfpl["low"],
            close=dfpl["close"],
        )
    ]
)

# plotting support lines
for i in range(len(ss)):
    fig.add_shape(
        type="line",
        x0=ss[i][0],
        y0=ss[i][1],
        x1=len(dfpl) - 1,
        y1=ss[i][1],
        line=dict(color="MediumPurple", width=2),
    )

# plotting resistance lines
for i in range(len(rr)):
    fig.add_shape(
        type="line",
        x0=rr[i][0],
        y0=rr[i][1],
        x1=len(dfpl) - 1,
        y1=rr[i][1],
        line=dict(color="RoyalBlue", width=2),
    )

fig.show()
