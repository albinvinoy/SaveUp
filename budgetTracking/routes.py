from flask import render_template, url_for
from budgetTracking import app, db, bcrypt
from budgetTracking.forms import RegisterForm, LoginForm
from budgetTracking.models import User

@app.route("/")
@app.route("/welcome")
def home():
    return render_template('welcome.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #if user and password match then log in the user
            return render_template("welcome.html")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            #add the user to the database
            password_hash = bcrypt.generate_password_hash(form.password.data)
            checkPassword = bcrypt.check_password_hash(password_hash, form.confirmPassword.data)
            if checkPassword:
                user = User(username=form.username.data, password=password_hash)
                db.session.add(user)
                db.session.commit()
                return render_template("welcome.html")
    return render_template("register.html", form=form)