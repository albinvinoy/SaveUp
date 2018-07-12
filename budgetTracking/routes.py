from flask import render_template, url_for
from budgetTracking import app, db
from budgetTracking.forms import RegisterForm, LoginForm

@app.route("/")
@app.route("/welcome")
def home():
    return render_template('welcome.html')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form=form)