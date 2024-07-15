from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .models import *
from . import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from collections import namedtuple

main = Blueprint('main', __name__)
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@main.route("/")
@main.route("/home")
def home():
    coinList = sorted(Stock.query.all(), key=lambda x: x.price, reverse=True)
    return render_template('index.html', coinList=coinList)


@main.route("/wallet/<user_id>", methods=['GET'])
def wallet(user_id):
    user = db.session.query(User).filter_by(user_id_tg=user_id).first()
    userstock = db.session.query(UserStock).filter_by(user_id=user.id).all()
    result = []
    node = namedtuple('node', ['name', 'price', 'quantity', 'total'])
    for coin in userstock:
        stock = db.session.query(Stock).filter_by(id=coin.stock_id).first()
        result.append(node(name=stock.name, price=stock.price, quantity=coin.quantity, total=stock.price * coin.quantity))

    result = sorted(result, key=lambda x: x.total, reverse=True) 
    return render_template('wallet.html', coinlist=result)


@main.route("/coin/<coin_id>", methods=['GET'])
def coin(coin_id):
    coin = db.session.query(Stock).filter_by(id=coin_id).first()
    if not coin:
        return redirect(url_for('main.home'))
    
    return render_template('coin.html', coin=coin)

@main.route("/get_user_tg", methods=['POST'])
def get_user_tg():
    user_id = request.form['user_id']
    user = db.session.query(User).filter_by(user_id_tg=user_id).first()
    if not user:
        user = User(user_id_tg=user_id)
        db.session.add(user)
        db.session.commit()

    return jsonify({'user_id': user_id, 'balance': user.balance})

@main.route("/buy", methods=['POST'])
def buy():
    user_id = request.form['user_id']
    stock_id = request.form['stock_id']
    quantity = int(request.form['quantity'])

    user = db.session.query(User).filter_by(user_id_tg=user_id).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'})

    stock = db.session.query(Stock).filter_by(id=stock_id).first()
    if not stock:
        return jsonify({'status': 'error', 'message': 'Stock not found'})
    
    if not user.check_balance(float(stock.price) * quantity):
        return jsonify({'status': 'error', 'message': 'Not enough balance'})

    user.update_balance(float(stock.price) * quantity)
    if db.session.query(UserStock).filter_by(user_id=user.id, stock_id=stock.id).first():
        userstock = db.session.query(UserStock).filter_by(user_id=user.id, stock_id=stock.id).first()
        userstock.update_quantity(quantity)
    else:
        userstock = UserStock(user_id=user.id, stock_id=stock.id, quantity=quantity)
        db.session.add(userstock)

    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Stock bought successfully'})


@main.route("/sell", methods=['POST'])
def sell():
    user_id = request.form['user_id']
    stock_id = request.form['stock_id']
    quantity = int(request.form['quantity'])

    user = db.session.query(User).filter_by(user_id_tg=user_id).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'})

    userstock = db.session.query(UserStock).filter_by(user_id=user.id, stock_id=stock_id).first()
    if not userstock:
        return jsonify({'status': 'error', 'message': 'Stock not found'})
    
    if userstock.quantity < quantity:
        return jsonify({'status': 'error', 'message': 'Not enough quantity'})

    stock = db.session.query(Stock).filter_by(id=stock_id).first()
    price = stock.price

    user.update_balance(-float(price) * quantity)
    userstock.update_quantity(-quantity)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Stock sell successfully'})

    

# @main.route('/user_page')
# @login_required
# def user_page():
#     data = {}
#     for device in db.session.query(Device).filter_by(user_id=current_user.id):
#         if device.name == "__hide__":
#             continue

#         if device.status_work == 1:
#             result = device.work()
#             if not result[0]:
#                 flash(result[1], 'error')
#         data[device] = db.session.query(Sensor).filter_by(device_id=device.id).all()
        
#     return render_template('user_page.html', username=current_user.username, data=data)


# @main.route("/register", methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form["username"]
#         password = request.form["password"]
#         user = User(username=username, password=password)
#         db.session.add(user)
#         db.session.commit()
#         login_user(user)
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('main.user_page'))
#     return render_template('register.html')

# @main.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form["username"]
#         password = request.form["password"]
#         user = db.session.query(User).filter_by(username=username, password=password).first()
#         if user:
#             login_user(user)
#             return redirect(url_for('main.user_page'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html')

# @main.route("/logout", methods=['POST'])
# def logout():
#     logout_user()
#     return render_template('login.html')
   