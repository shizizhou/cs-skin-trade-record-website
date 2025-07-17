import csv
import io
import time
import flask
from flask import request, render_template, redirect, url_for,abort
from database import SessionLocal, engine
from model import Trade, User
from sqlalchemy import desc
from sqlalchemy.orm import Session
from init_db import init_database
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os

ip_register_time = {}

#初始化数据库
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 
app.secret_key = 'aabbccddeeffgghh'
init_database()


#设置登陆功能
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    return session.query(User).get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    ip = request.remote_addr
    now = time.time()
    last_time = ip_register_time.get(ip, 0)
    if now - last_time < 60:
        abort(429, "注册太频繁，请稍后再试")
    ip_register_time[ip] = now
    
    if request.method == 'POST':
        session = SessionLocal()
        username = request.form['username']
        password = request.form['password']

        if session.query(User).filter_by(username=username).first():
            return render_template('register_failed.html', message="用户名已存在，请选择其他用户名。")
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        return render_template('register_success.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = SessionLocal()
        username = request.form['username']
        password = request.form['password']

        user = session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/')
        return render_template('login_failed.html')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#辅助方法
def get_all_trades():
    db: Session = SessionLocal()
    trades = db.query(Trade).filter_by(user_id=current_user.id).all()
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
        user_id=trade_dict["user_id"]
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


#主页面逻辑
@app.route("/")
@login_required
def index():
    trades = get_all_trades()
    total_trades = len(trades)
    total_income = sum(trade.net_income for trade in trades)
    total_purchase_price = sum(trade.purchase_price for trade in trades)
    total_sell_price = sum(trade.sell_price for trade in trades)
    return render_template("index.html", trades=trades, total_trades=total_trades, total_income=total_income, total_purchase_price=total_purchase_price, total_sell_price=total_sell_price)

@app.route("/add_trade", methods=["GET"])
@login_required
def add_trade_form():
    return render_template("add_trade.html")

@app.route("/add_trade", methods=["POST"])
@login_required
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
    trade = {
        "name": request.form["name"],
        "float": request.form["float"],
        "purchase price": purchase_price,
        "sell price": sell_price,
        "gross income": gross_income,
        "net income": net_income,
        "user_id": current_user.id
    }

    add_trade(trade)
    return redirect(url_for("index"))

@app.route("/delete_trade", methods=["POST"])
@login_required
def delete_trade():
    name = request.form["name"]
    purchase_price = float(request.form["purchase_price"])
    sell_price = float(request.form["sell_price"])
    delete_trade_by_info(name, purchase_price, sell_price)
    return redirect(url_for("index"))

@app.route("/profit")
@login_required
def profit():
    db: Session = SessionLocal()
    trades = db.query(Trade).filter(Trade.net_income >= 0).filter_by(user_id=current_user.id).order_by(Trade.net_income.desc()).all()
    total_income = sum(trade.net_income for trade in trades)
    db.close()
    return render_template("profit.html", trades=trades, total_income=total_income)

@app.route("/loss")
@login_required
def loss():
    db: Session = SessionLocal()
    trades = db.query(Trade).filter(Trade.net_income < 0).filter_by(user_id=current_user.id).order_by(Trade.net_income).all()
    total_loss = sum(trade.net_income for trade in trades)
    db.close()
    return render_template("loss.html", trades=trades, total_loss=total_loss)

@app.route("/search", methods=["GET"])
@login_required
def search():
    q = request.args.get('q', '').strip()
    trades = []
    if q:
        session = SessionLocal()
        trades = session.query(Trade)\
            .filter(Trade.name.ilike(f"%{q}%"))\
            .filter_by(user_id=current_user.id)\
            .order_by(desc(Trade.id))\
            .all()
        session.close()
    count = len(trades)
    return render_template('search.html', trades=trades, q=q, count=count)

@app.route("/import_csv", methods=["GET", "POST"])
@login_required
def import_csv_route():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename.endswith('.csv'):
            return "请上传一个有效的CSV文件。"

        try:
            content = file.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(content))
            for row in reader:
                row["name"] = row["name"].strip() if row["name"] else ""
                row["float"] = row["float"] if row["float"] else 0.0
                row["purchase price"] = float(row["purchase price"]) if row["purchase price"] else 0.0
                row["sell price"] = float(row["sell price"]) if row["sell price"] else 0.0
                row["gross income"] = float(row["gross income"]) if row["gross income"] else 0.0
                row["net income"] = float(row["net income"]) if row["net income"] else 0.0
                row["user_id"] = current_user.id
                add_trade(row)
            return redirect(url_for("index"))
        except Exception as e:
            return f"导入失败: {e}", 500

    return render_template("import_csv.html")

@app.route("/export")
@login_required
def export():
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'name', 'float', 'purchase price', 'sell price',
        'gross income', 'net income'
    ])

    trades = get_all_trades()

    for t in trades:
        writer.writerow([
            t.name,
            t.float_value,
            t.purchase_price,
            t.sell_price,
            t.gross_income,
            t.net_income
        ])

    response = flask.Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=trades_export.csv'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)