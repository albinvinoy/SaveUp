from flask import render_template
from budgetTracking import app, db

@app.route("/")
@app.route("/welcome")
def home():
    return render_template('welcome.html')