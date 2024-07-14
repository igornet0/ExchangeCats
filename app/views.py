from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .forms import RegistrationForm, LoginForm
from .models import *
from . import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .error import *
from .Api_devices import *

main = Blueprint('main', __name__)
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.user_page'))  # Перенаправить на главную страницу для залогиненных пользователей
    return render_template('login.html')

@main.route('/user_page')
@login_required
def user_page():
    data = {}
    for device in db.session.query(Device).filter_by(user_id=current_user.id):
        if device.name == "__hide__":
            continue

        if device.status_work == 1:
            result = device.work()
            if not result[0]:
                flash(result[1], 'error')
        data[device] = db.session.query(Sensor).filter_by(device_id=device.id).all()
        
    return render_template('user_page.html', username=current_user.username, data=data)


@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.user_page'))
    return render_template('register.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = db.session.query(User).filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('main.user_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@main.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return render_template('login.html')
   