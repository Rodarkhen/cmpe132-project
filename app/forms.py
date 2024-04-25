# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

# Define possible roles
ROLES = [('student', 'Student'), ('faculty', 'Faculty'), ('librarian', 'Librarian')]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=25)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=25)])
    username = StringField('Username', validators=[DataRequired() ]) #, Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired() ]) #, Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=ROLES, validators=[DataRequired()])
    submit = SubmitField('Register')
