"""
This module contains the structure of all of the forms used on the app.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    """WTForm for sign up page."""
    first_name = StringField('First name', validators=[
        DataRequired('Please enter your first name.')])
    last_name = StringField('Last name', validators=[
        DataRequired('Please enter your last name.')])
    email = StringField('Email', validators=[
        DataRequired('Please enter your email.'),
        Email('Please enter a valid email.')])
    username = StringField('Username', validators=[
        DataRequired('Please enter a username.')])
    password = PasswordField('Password', validators=[
        DataRequired('Please enter a password.'),
        Length(min=6, message='Passwords must have at least 6 characters.')])

    role_choices = [(0, 'Choose Role'),
                    (2, 'Unassigned'),
                    (3, 'Judge'),
                    (4, 'Singer'),
                    (5, 'Artist'),
                    (6, 'Mixer'),
                    (7, 'Animator')]

    role = SelectField('Role', coerce=int, choices=role_choices, validators=[
        DataRequired('Please choose a role.')])
    print(role)

    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    """WTForm for login page."""
    username = StringField('Username', validators=[DataRequired('Please enter your username.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.')])
    submit = SubmitField('Sign in')

class CreateChorusBattleForm(FlaskForm):
    """WTForm for creating a chorus battle."""
    name = StringField('Name of Chorus Battle', validators=[
        DataRequired('Please enter a name for your chorus battle.')])
    description = TextAreaField('Description', validators=[
        DataRequired('Please provide a brief description of your chorus battle.')])
    # it would be nice if there was a stringfield for each separate rule
    # and the user is able to add a stringfield by clicking a button if more rules are needed
    rules = TextAreaField('List of Rules', validators=[
        DataRequired('Please provide a list of rules that participants must follow or know about.')])
    prizes = TextAreaField('Prizes', validators=[
        DataRequired('Please provide a list of prizes that participants can win from the chorus battle, if there are any.')])
    video_link = StringField('Link to the Chorus Battle Introduction Video')
    submit = SubmitField('Create Chorus Battle')

class CreateRoundForm(FlaskForm):
    """WTForm for adding a round for a particular chorus battle."""
    round_number = IntegerField('Round Number', validators=[
        DataRequired('Please enter the round number.')])
    theme = TextAreaField('Theme', validators=[
        DataRequired('Please enter the theme for this particular round.')])
    deadline = DateTimeField('Deadline', validators=[
        DataRequired('Please enter the deadline (date and time) for this round.')])
    submit = SubmitField('Create New Round')
