from cs50 import SQL
from flask import session

db = SQL("sqlite:///finance.db")


def do_restart():
    db.execute("DELETE FROM orders")
    db.execute("DELETE FROM users")
    db.execute("UPDATE sqlite_sequence SET seq = 0")

    return 0


def insert_user(username, password_hash):
    id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
    return id


def get_bought():
    return db.execute("SELECT symbol, sum(shares) AS shares, sum(price * shares) AS amount FROM orders WHERE user_id = ? AND type_id = ? GROUP BY symbol ORDER BY id", session.get('user_id'), 1)


def get_cash():
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session.get('user_id'))
    if len(user_cash) != 0:
        return round(user_cash[0]["cash"], 2)
    else:
        return 0


def get_orders():
    return db.execute("SELECT a.symbol, a.type_id, b.tx_type, a.shares, a.price, (a.price * a.shares) AS amount, timestamp FROM orders a, type_orders b WHERE a.user_id = ? AND a.type_id = b.id ORDER BY a.id", session.get('user_id'))


def get_sold():
    return db.execute("SELECT symbol, sum(shares) AS shares, sum(price * shares) AS amount FROM orders WHERE user_id = ? AND type_id = ? GROUP BY symbol ORDER BY id", session.get('user_id'), 2)


def get_user(username):
    return db.execute("SELECT * FROM users WHERE username = ?", username)


def insert_order(type_id, symbol, shares, float_price):
    return db.execute("INSERT INTO orders (user_id, type_id, symbol, shares, price) VALUES (?, ?, ?, ?, ?)", session.get('user_id'), type_id, symbol, shares, float_price)


def update_cash(float_total):
    return db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", float_total, session.get('user_id'))
