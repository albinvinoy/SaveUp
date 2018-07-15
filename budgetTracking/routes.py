from flask import render_template, url_for, request, redirect, flash
from budgetTracking import app, db, bcrypt, login_manager
from budgetTracking.forms import RegisterForm, LoginForm, ExpenseForm, IncomeForm
from budgetTracking.models import User
from flask_login import login_user, current_user, logout_user, login_required

'''
Need to figure out why userLoader is needed
UserMix 
'''
@login_manager.user_loader
def user_loader(user_id):
    '''Given user_id return User Object
    :param int user_id
    '''
    return User.query.get(user_id)


@app.route("/")
@app.route("/welcome")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('summary'))
    return render_template('welcome.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('summary'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #if user and password match then log in the user
            login_user(user, remember=True)
            next = request.args.get("next")
            return redirect(next) if next else redirect(url_for('summary'))
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


@app.route('/updateAccount', methods=["GET", "POST"])
@login_required
def updateAccount():
    '''
        This will need login info of the user
        This will add and remove transactions
    '''
    form = ExpenseForm()
    if request.method == "POST":
        if request.form.get("btn")=="Expense":
            print("in expense")
            form = ExpenseForm()
        elif request.form.get("btn")=="Income":
            print("in income")
            form = IncomeForm()  
        else:
            if request.form["submit"]=="Add Expenses":
                print("in Add Expenses")
                return redirect(url_for('updateAccount'))
            else:
                print("in Add Income")
                return redirect(url_for('updateAccount'))     

    return render_template("budgetTrack.html", form=form)


@app.route('/summary')
@login_required
def summary():
    user = User.query.filter_by(username=current_user.username).first()
    '''
        This will need login info of the user
        This will show user details based on filters(?)
    '''
    return render_template("summary.html", user=user)


@app.route('/logout')
def logout():
    logout_user()
    return render_template("welcome.html")

