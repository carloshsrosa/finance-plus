import datetime
import json
import os
from cs50 import SQL
from databases import get_bought, get_sold, get_orders
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.dates import date2num, DateFormatter
import yfinance as yf
from datetime import datetime


from flask import redirect, render_template, session
from functools import wraps

db = SQL("sqlite:///finance.db")


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    # Prepare API request

    symbol = symbol.upper()
    data = yf.Ticker(symbol)

    price = data.history(period="1d")['Close'][0]

    return {"price": price, "symbol": symbol}


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def get_cash():
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session.get('user_id'))

    return round(user_cash[0]["cash"], 2)


def get_stocks():

    stocks_bought = get_bought()
    stocks_sold = get_sold()

    orders = []

    if len(stocks_bought) != 0:
        for bought in stocks_bought:
            order = {}
            if len(stocks_sold) != 0:
                for sold in stocks_sold:
                    if bought['symbol'] == sold['symbol']:
                        order['symbol'] = bought['symbol']
                        order['shares'] = bought['shares'] - sold['shares']
                        order['amount'] = bought['amount'] - sold['amount']
                        if order['shares'] > 0:
                            orders.append(order)
                if len(order) == 0:
                    order['symbol'] = bought['symbol']
                    order['shares'] = bought['shares']
                    order['amount'] = bought['amount']
                    if order['shares'] > 0:
                        orders.append(order)

            else:
                order['symbol'] = bought['symbol']
                order['shares'] = bought['shares']
                order['amount'] = bought['amount']
                if order['shares'] > 0:
                    orders.append(order)

    id = 0
    if len(orders) != 0:
        for order in orders:
            symbol = order["symbol"]
            order["float_amount"] = order["amount"]
            order["amount"] = usd(order["amount"])
            order["sell_shares"] = 0
            order["sell_total"] = usd(0)
            id += 1
            order["id"] = id
            if not lookup(symbol):
                return apology("Internal Server Error", 500)
            else:
                current_price = lookup(symbol)["price"]
                order["float_price"] = current_price
                order["current_price"] = usd(current_price)

    return orders


def stocks_history():

    orders = get_orders()

    if len(orders) != 0:
        for order in orders:
            price = usd(order["price"])
            order["price"] = price
            amount_float = order["amount"]
            order["float_amount"] = amount_float
            if order["type_id"] == 1:
                order["float_amount"] = amount_float * -1
            order["amount"] = usd(amount_float)

    return orders


def do_candle(symbol):

    # Prepare API request
    symbol = symbol.upper()
    data = yf.Ticker(symbol)

    historical_data = data.history(period="3mo")

    data_json = json.loads(historical_data.to_json(orient="index"))

    list_date = []
    list_open = []
    list_high = []
    list_low = []
    list_close = []
    list_volume = []
    for date, items in data_json.items():
        timestamp = int(date) // 1000
        data = datetime.fromtimestamp(timestamp)
        data_formatada = data.strftime('%Y-%m-%d')
        list_date.append(data_formatada)
        list_open.append(float(items['Open']))
        list_high.append(float(items['High']))
        list_low.append(float(items['Low']))
        list_close.append(float(items['Close']))
        list_volume.append(float(items['Volume']))

    data = {}

    data["date"] = list_date
    data["open"] = list_open
    data["high"] = list_high
    data["low"] = list_low
    data["close"] = list_close
    data["volume"] = list_volume

    data = json.dumps(data)

    # Criar DataFrame
    df = pd.read_json(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Criar o gráfico de velas
    id = str(session.get('user_id'))
    image = (f"static/" + id + "_stock_prices.png")

    if os.path.exists(image):
        os.remove(image)

    # Configurações do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Converter DataFrame para o formato necessário
    quotes = [tuple([date2num(date)] + list(quote))
                for date, quote in zip(df.index, df[['open', 'high', 'low', 'close']].values)]

    # Configurar o estilo de velas
    candlestick_ohlc(ax, quotes, width=0.6, colorup='g', colordown='r')

    # Configurar título e rótulos
    ax.set_title('Candle Chart')
    ax.set_ylabel('Price')
    ax.set_xlabel('Date')

    # Formatar as datas no eixo x
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    # Adicionar grid
    plt.grid(True)

    # Salvar o gráfico em um arquivo
    plt.savefig(image)

    return image
