from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'budget.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#
# export FLASK_APP=budgetTracking
#flask shell
#from budgetTracking import db
#db.create_all()
#

from budgetTracking import routes, models
