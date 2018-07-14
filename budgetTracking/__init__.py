from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import os
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'budget.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

#
# export FLASK_APP=budgetTracking
#flask shell
#from budgetTracking import db
#db.create_all()
#

from budgetTracking import routes, models
