import flask
from flask import request, render_template, redirect, url_for
from database import SessionLocal, engine
from model import Trade
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from init_db import init_database, import_csv
import os

app = flask.Flask(__name__)
init_database()
import_csv()

def get_all_trades():
    db: Session = SessionLocal()
    trades = db.query(Trade).all()
    db.close()
    return trades

def add_trade(trade_dict):
    db: Session = SessionLocal()
    trade = Trade(
        name=trade_dict["name"],
        float_value=trade_dict["float"],
        purchase_price=trade_dict["purchase price"],
        sell_price=trade_dict["sell price"],
        gross_income=trade_dict["gross income"],
        net_income=trade_dict["net income"],
        total_income=trade_dict["total income"]
    )
    db.add(trade)
    db.commit()
    db.close()

def delete_trade_by_info(name, purchase_price, sell_price):
    db: Session = SessionLocal()
    trade = db.query(Trade).filter(
        Trade.name == name,
        Trade.purchase_price == purchase_price,
        Trade.sell_price == sell_price
    ).first()
    if trade:
        db.delete(trade)
        db.commit()
    db.close()

@app.route("/")
def index():
    trades = get_all_trades()
    total_trades = len(trades)
    total_income = trades[-1].total_income if trades else 0
    total_purchase_price = sum(trade.purchase_price for trade in trades)
    total_sell_price = sum(trade.sell_price for trade in trades)
    return render_template("index.html", trades=trades, total_trades=total_trades, total_income=total_income, total_purchase_price=total_purchase_price, total_sell_price=total_sell_price)

@app.route("/add_trade", methods=["GET"])
def add_trade_form():
    return render_template("add_trade.html")

@app.route("/add_trade", methods=["POST"])
def add_trade_route():
    purchase_price = float(request.form["purchase_price"])
    sell_price = float(request.form["sell_price"])
    gross_income = sell_price - purchase_price

    platform = request.form.get("trade_type")
    if platform == "buff":
        net_income = sell_price * 0.975 - purchase_price
    elif platform == "youyou":
        net_income = sell_price * 0.99 - purchase_price
    else:
        net_income = sell_price * 0.98 - purchase_price
    net_income = round(net_income, 2)
    trades = get_all_trades()
    if trades:
        total_income = trades[-1].total_income
    else:
        total_income = 0
    total_income = round(total_income + net_income, 2)
    trade = {
        "name": request.form["name"],
        "float": request.form["float"],
        "purchase price": purchase_price,
        "sell price": sell_price,
        "gross income": gross_income,
        "net income": net_income,
        "total income": total_income
    }

    add_trade(trade)
    return redirect(url_for("index"))

@app.route("/delete_trade", methods=["POST"])
def delete_trade():
    name = request.form["name"]
    purchase_price = float(request.form["purchase_price"])
    sell_price = float(request.form["sell_price"])
    delete_trade_by_info(name, purchase_price, sell_price)
    return redirect(url_for("index"))


@app.route("/profit")
def profit():
    db: Session = SessionLocal()
    trades = db.query(Trade).filter(Trade.net_income >= 0).order_by(desc(Trade.net_income)).all()
    total_income = sum(trade.net_income for trade in trades)
    db.close()
    return render_template("profit.html", trades=trades, total_income=total_income)

@app.route("/loss")
def loss():
    db: Session = SessionLocal()
    trades = db.query(Trade).filter(Trade.net_income < 0).order_by(Trade.net_income).all()
    total_loss = sum(trade.net_income for trade in trades)
    db.close()
    return render_template("loss.html", trades=trades, total_loss=total_loss)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)