from budgetTracking import db
from datetime import datetime


class User(db.Model):
    # Table for user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profilePicture = db.Column(db.String(20), nullable=False, default='default.jpg')
    incomes = db.relationship('Income', backref='user')
    expenses = db.relationship('Expense', backref='user')

    def __repr__(self):
        return "{} {}".format(self.username, self.email)


class Expense(db.Model):
    # Table that shows expense of the user
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False)
    #connect this to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "{} {}".format(self.amount, self.postedDate)

class Income(db.Model):
    # Table that shows income of the user
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    postedDate = db.Column(db.DateTime, nullable=False)
    #connect this to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "{} {}".format(self.amount, self.postedDate)