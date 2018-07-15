from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from budgetTracking.models import User

#Budget Tracking
class ExpenseForm(FlaskForm):
    name = StringField("Store Name", validators=[DataRequired(), Length(min=2, max=20 )])
    amount = DecimalField("Amount", validators=[DataRequired()], places=2)
    #picture
    category = SelectField(label="Category",choices=[ 
        ("Gas", "Gas"),
        ("Gadgets", "Gadgets"),
        ("Insurance", "Insurance"),
        ("Food", "Food"),
        ("Movie", "Movie"),
        ("Entertainment", "Entertainment"),
        ("Bill", "Bill"),
        ("Office Supplies", "Office Supplies"),
        ("Grocery", "Grocery"),
        ("Mortgage", "Mortgage"),
        ("Repair", "Repair"),
        ("Online", "Online"),
        ("Clothing", "Clothing"),
        ("Accommodation","Accommodation"),
        ("Taxi", "Taxi")
        ])

    payment = SelectField(label="Payment", validators=[DataRequired()], choices=[
        ("cash", "Cash"),
        ("card", "Card")])

    location = StringField("Location", validators=[Length(min=2, max=20)])
    date = StringField("Date", validators=[DataRequired()])
    submit = SubmitField("Add Expenses")

class IncomeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20 )])
    amount = DecimalField("Amount", validators=[DataRequired()], places=2)
    #picture
    category = SelectField(label="Category",choices=[ ("Income", "Income") ])
    payment = SelectField(label="Payment Method", choices=[
        ("dd", "Direct Deposit"),
        ("check", "Check")])
    date = StringField("Date", validators=[DataRequired()])

    submit = SubmitField("Add Income")
#Login and registration

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken")


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

    #Every time the form is submitted these functions are triggered, 
    # #if commented then code should handle it
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("Error Logging in")