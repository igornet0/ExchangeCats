from random import randint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import numpy 
import datetime
from . import db

def delete_data(db):
    try:
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        print("All data deleted.")
    except Exception as e:
        db.session.rollback()
        print("Failed to delete data:", e)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_tg = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def update_balance(self, new_balance):
        self.balance = new_balance

    def check_balance(self, amount):
        return self.balance >= amount

    def __repr__(self):
        return f"<User {self.id} user_id_tg: {self.user_id_tg} balance: {self.balance}>"

class UserStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    stock_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<UserStock {self.id} user_id: {self.user_id} stock_id: {self.stock_id} quantity: {self.quantity}>"

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Stock {self.id} name: {self.name} price: {self.price} quantity: {self.quantity}>"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    stock_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Transaction {self.id} user_id: {self.user_id} stock_id: {self.stock_id} quantity: {self.quantity} price: {self.price} date: {self.date}>"

