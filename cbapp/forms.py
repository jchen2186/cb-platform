from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
    first_name = StringField('First name', 
        validators=[DataRequired('Please enter your first name.')])
    last_name = StringField('Last name', 
        validators=[DataRequired('Please enter your last name.')])
    email = StringField('Email', 
        validators=[DataRequired('Please enter your email.'),
        Email('Please enter a valid email.')])
    username = StringField('Username', 
        validators=[DataRequired('Please enter a username.')])
    password = PasswordField('Password', 
        validators=[DataRequired('Please enter a password.'),
        Length(min=6,  message='Passwords must have at least 6 characters.')])
    # change this later to specify the possible roles the user can be
    role = StringField('Role')
        # validators=[DataRequired('Please enter your role.')])
    submit = SubmitField('Sign up')

class LoginForm(Form):
    username = StringField('Username', 
        validators=[DataRequired('Please enter your username.')])
    password = PasswordField('Password', 
        validators=[DataRequired('Please enter your password.')])
    submit = SubmitField('Sign in')