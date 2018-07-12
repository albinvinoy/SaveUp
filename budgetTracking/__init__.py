from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "wGoJpC9H36FRK3hPhGMnncHKtrcG0M7cSxcbbdzCPkOlQNgK0FSIAEzuS7Rv35b0"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///track.db"
db = SQLAlchemy(app)


from budgetTracking import routes
