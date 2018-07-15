from budgetTracking import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # Table for user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    profilePicture = db.Column(db.String(20), nullable=False, default='default.jpg')
    incomes = db.relationship('Income', backref='user')
    expenses = db.relationship('Expense', backref='user')

    def __repr__(self):
        return "{}".format(self.username)


class Expense(db.Model):
    # Table that shows expense of the user
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False )
    #add pic later
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(25))
    payment = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(50))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    #connect this to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "{} {}".format(self.amount, self.postedDate)

class Income(db.Model):
    # Table that shows income of the user
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False )
    #pic here
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(25))
    payment = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #connect this to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "{} {}".format(self.amount, self.postedDate)