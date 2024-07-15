from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
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
    balance = db.Column(db.Float, nullable=False, default=50000)

    def update_balance(self, new_balance):
        self.balance -= new_balance

    def check_balance(self, amount: int) -> bool:
        return self.balance >= amount

    def __repr__(self):
        return f"<User {self.id} user_id_tg: {self.user_id_tg} balance: {self.balance}>"

class UserStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    stock_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def update_quantity(self, new_quantity):
        self.quantity += new_quantity

        if self.quantity <= 0:
            db.session.delete(self)

    def __repr__(self):
        return f"<UserStock {self.id} user_id: {self.user_id} stock_id: {self.stock_id} quantity: {self.quantity}>"

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    def default_stocks():
        if db.session.query(Stock).count() > 0:
            return
        
        default_stocks = [{"name": "BitCats", "price": 50000, "quantity": 100}, 
                          {"name": "EthCats", "price": 1000, "quantity": 1000}, 
                          {"name": "TonCats", "price": 7, "quantity": 1000}, 
                          {"name": "XmrCats", "price": 150, "quantity": 1000}, 
                          {"name": "WerCats", "price": 10, "quantity": 1000}, 
                          {"name": "RicCats", "price": 1, "quantity": 1000}]

        for stock in default_stocks:
            new_stock = Stock(name=stock["name"], price=stock["price"], quantity=stock["quantity"])
            db.session.add(new_stock)
        db.session.commit()

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

