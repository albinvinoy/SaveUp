from flask import render_template, url_for, request, redirect, flash, jsonify
from budgetTracking import app, db, bcrypt, login_manager
from budgetTracking.forms import RegisterForm, LoginForm, ExpenseForm, IncomeForm
from budgetTracking.models import User, Expense, Income
from flask_login import login_user, current_user, logout_user, login_required


from datetime import datetime
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


'''
Helper functions
'''

def expenseAdder(form):
    return Expense(
        name=form.name.data,
        amount=form.amount.data,
        category=form.category.data,
        paymentMethod=form.payment.data,
        location=form.location.data,
        date=datetime.utcnow(),
        user_id=current_user.id)

def incomeAdder(form):
    return Income(
        name=form.name.data,
        amount=form.amount.data,
        category=form.category.data,
        paymentMethod=form.payment.data,
        date=datetime.utcnow(),
        user_id=current_user.id)

'''
Application routes
'''

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
            checkPassword = True if form.password.data == form.confirmPassword.data else False
            if checkPassword:
                password_hash = bcrypt.generate_password_hash(form.password.data)
                user = User(username=form.username.data, password=password_hash)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('register'))
    return render_template("register.html", form=form)


@app.route('/updateTransactions', methods=["GET", "POST"])
@login_required
def updateTransactions():
    '''
        This will need login info of the user
        This will add and remove transactions
    '''
    form = ExpenseForm()
    if request.method == "POST":
        if request.form.get("btn")=="Expense":
            form = ExpenseForm()
        elif request.form.get("btn")=="Income":
            print("in income")
            form = IncomeForm()  
        else:
            if request.form["submit"]=="Add Expenses":
                expense = expenseAdder(form)
                db.session.add(expense)
                db.session.commit()
                # flash("Expense Added")
                #this is to stop page from resubmitting information
            elif request.form["submit"]=="Add Income":
                income = incomeAdder(form)
                db.session.add(income)
                db.session.commit()
                # flash("Income Added")
            else:
                redirect(url_for('logout'))
            return redirect(url_for('updateTransactions'))     

    return render_template("budgetTrack.html", form=form)


@app.route('/summary', methods=["GET", "POST"])
@login_required
def summary():
    #post
    if request.method=="POST":
        user = User.query.filter_by(username=current_user.username).first()

        if request.form.get("fetchData")=="Expense":
            expenseQuery = Expense.query.filter_by(user_id=user.id)
            contentData = [e.toJson() for e in expenseQuery]
            return render_template("summary.html", user=user, requestType="Expense", contentData=contentData)

            #query the expense from database
            
        elif request.form.get("fetchData")=="Income":
            #query the income from database
            incomeQuery = Income.query.filter_by(user_id=user.id)
            contentData = [e.toJson() for e in incomeQuery]
            return render_template("summary.html", user=user, requestType="Income", contentData=contentData)

        else:
            #make a get request to summary
            return redirect(url_for('summary'))

    #get
    else:
        #This needs to change to show both income and expenses
        user = User.query.filter_by(username=current_user.username).first()
        expenseQuery = Expense.query.filter_by(user_id=user.id)
        contentData = [e.toJson() for e in expenseQuery]
        '''
            This will need login info of the user
            This will show user details based on filters(?)
        '''
        return render_template("summary.html", user=user, requestType='', contentData=contentData)


@app.route("/delete/<int:ids>/<typeName>")
@login_required
def delete(ids, typeName):
    print(typeName, ids)
    if typeName=='':
        return (''), 204
    else:
        if typeName=="Income":
            Income.query.filter_by(id=ids).delete()
            print(Income.query.all())
            user = User.query.filter_by(username=current_user.username).first()

            incomeQuery = Income.query.filter_by(user_id=user.id)

            print(incomeQuery, user.id)
            contentData = [e.toJson() for e in incomeQuery]
            print(contentData)
        elif typeName=="Expense":
            Expense.query.filter_by(id=ids).delete()
        return redirect(url_for('summary'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("welcome.html")

