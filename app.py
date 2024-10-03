from databases import do_restart, insert_user, get_cash, get_user, insert_order, update_cash
import os
import glob
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, do_candle, login_required, usd, get_stocks, stocks_history, lookup

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    orders = get_stocks()

    if len(orders) == 0:
        flash(f"No Stocks")

    cash = usd(get_cash())

    return render_template("index.html", orders=orders, cash=cash)


@app.route("/restart")
def restart():

    do_restart()

    directory = 'static'

    png_files = glob.glob(os.path.join(directory, '*stock_prices.png'))

    for file in png_files:
        os.remove(file)

    return redirect("/logout")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get('symbol'):
            return apology("must provide a symbol", 403)

        symbol = request.form.get('symbol').upper()

        if not lookup(symbol):
            return apology("invalid symbol", 400)

        float_price = lookup(symbol)["price"]
        price = usd(float_price)

        float_cash = get_cash()
        cash = usd(float_cash)

        max_shares = int(int(float_cash) / int(float_price))
        return render_template("buy.html", symbol=symbol, price=price, cash=cash, float_price=float_price, float_cash=float_cash, max_shares=max_shares)

    cash = usd(get_cash())

    return render_template("buy.html", cash=cash)


@app.route("/bought", methods=["POST"])
@login_required
def bought():
    if not request.form.get('symbol'):
        return apology("must provide a symbol", 403)

    symbol = request.form.get('symbol').upper()

    if not lookup(symbol):
        return apology("invalid symbol", 400)

    if not request.form.get('float_price'):
        return apology("must provide a price", 403)

    if not request.form.get('shares'):
        return apology("must provide shares", 403)

    float_price = float(request.form.get('float_price'))

    float_shares = float(request.form.get('shares'))

    float_total = float(float_price * float_shares)

    float_cash = get_cash()

    if float_total > float_cash:
        return apology("you don't have enough cash", 403)

    shares = int(float_shares)

    insert_order(1, symbol, shares, float_price)
    update_cash(float_total * -1)

    total = usd(float_total)
    flash(f"Bought {shares} shares of {symbol} for {total}")

    orders = get_stocks()

    if len(orders) == 0:
        flash(f"No Stocks")

    cash = usd(get_cash())

    return render_template("index.html", orders=orders, cash=cash)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    orders = stocks_history()

    if len(orders) == 0:
        flash(f"No Stocks")

    cash = usd(get_cash())

    return render_template("history.html", orders=orders, cash=cash)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        username = request.form.get("username")

        # Query database for username
        user = get_user(username)

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(
            user[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]
        session["username"] = username

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Forget any user_id
        session.clear()
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get('symbol'):
            return apology("must provide a symbol", 403)

        symbol = request.form.get('symbol').upper()

        if not lookup(symbol):
            return apology("invalid symbol", 400)

        price = usd(lookup(symbol)["price"])

        cash = usd(get_cash())

        return render_template("quote.html", symbol=symbol, price=price, cash=cash)

    cash = usd(get_cash())

    return render_template("quote.html", cash=cash)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        session.clear()

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        username = request.form.get("username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        password = request.form.get("password")

        # Ensure confirm_password was submitted
        if not request.form.get("confirm_password"):
            return apology("must provide confirm password", 403)

        confirm_password = request.form.get("confirm_password")

        # Ensure the password is the same as confirm password
        if password != confirm_password:
            return apology("confirm password does not match", 403)

        # Query database for username
        user = get_user(username)

        # Ensure username exists and password is correct
        if len(user) != 0:
            return apology("username already exists", 400)
        else:
            password_hash = generate_password_hash(password)

        # Insert into table users
        id = insert_user(username, password_hash)

        # Remember which user has logged in
        session["user_id"] = id
        session["username"] = username

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.getlist("id"):
            return apology("Internal Server Error", 500)

        ids = request.form.getlist("id")

        stocks = []
        amount = float(0)

        for id in ids:
            if not request.form.get("sell_shares_" + id):
                return apology("Internal Server Error", 500)

            sell_shares = request.form.get("sell_shares_" + id)

            if not request.form.get("symbol_" + id):
                return apology("Internal Server Error", 500)

            symbol = request.form.get("symbol_" + id)

            if not request.form.get("float_price_" + id):
                return apology("Internal Server Error", 500)

            float_price = request.form.get("float_price_" + id)

            if int(sell_shares) > 0:
                stock = {}
                stock["symbol"] = symbol
                stock["shares"] = sell_shares
                stock["price"] = float_price
                stocks.append(stock)
                amount = float(amount) + (float(float_price) * float(sell_shares))

        float_total = float(amount)

        shares_own = get_stocks()

        for order in stocks:
            symbol = order["symbol"]
            shares = int(order["shares"])
            float_price = float(order["price"])
            if len(shares_own) != 0:
                shares_owned = 0
                for share_own in shares_own:
                    if share_own["symbol"] == symbol:
                        shares_owned += 1
                        if shares <= share_own["shares"]:
                            insert_order(2, symbol, shares, float_price)
                        else:
                            return apology("you don't have enough shares", 403)
                if shares_owned == 0:
                    return apology("you don't have enough shares", 403)
            else:
                return apology("you don't have enough shares", 403)

        if len(stocks) != 0:
            update_cash(float_total)

            total = usd(float_total)

            flash(f"Sold shares for {total}")

            orders = get_stocks()

            float_cash = get_cash()
            cash = usd(get_cash())

            return render_template("index.html", cash=cash, orders=orders)

        orders = get_stocks()

        float_cash = get_cash()
        cash = usd(get_cash())

        return render_template("sell.html", cash=cash, orders=orders, float_cash=float_cash)

    orders = get_stocks()

    if len(orders) == 0:
        flash(f"No shares to sell")

    float_cash = get_cash()
    cash = usd(float_cash)

    return render_template("sell.html", cash=cash, orders=orders, float_cash=float_cash)


@app.route("/chart", methods=["GET", "POST"])
def chart():

    if request.method == "POST":

        if not request.form.get('symbol'):
            return apology("must provide a symbol", 403)

        symbol = request.form.get('symbol').upper()

        if not lookup(symbol):
            return apology("invalid symbol", 400)

        do_candle(symbol)
        id = str(session.get('user_id'))
        image = (f"static/" + id + "_stock_prices.png")

        float_cash = get_cash()
        cash = usd(float_cash)

        return render_template('chart.html', cash=cash, symbol=symbol, image=image)

    cash = usd(get_cash())

    return render_template("chart.html", cash=cash)
