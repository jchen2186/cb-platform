"""
This module contains the structure of all of the forms used on the app.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import TextAreaField, DateTimeField, IntegerField, FileField, ValidationError, FieldList
from wtforms.validators import DataRequired, Email, Length
from .models import User, ChorusBattle
from datetime import datetime
def validate_username(form, field):
    """
    Checks whether username is unique. If is not
    unique, it will raise a validation error.
    """
    if not User.is_username_unique(field.data):
        raise ValidationError('Username is taken. Please try another username.')

def validate_email(form, field):
    """
    Checks whether email is unique. If it is not
    unique, it will raise a validation error.
    """
    if not User.is_email_unique(field.data):
        raise ValidationError('There already exists an account with this email.')

def validate_username_exists(form, field):
    """
    Checks whether a username exists. If it 
    does not exist, it will raise a validation
    error.
    """
    if User.is_username_unique(field.data):
        raise ValidationError('This username does not exist.')

class SignupForm(FlaskForm):
    """
    WTForm for sign up page.
    """
    first_name = StringField('First name', validators=[
        DataRequired('Please enter your first name.')])
    last_name = StringField('Last name', validators=[
        DataRequired('Please enter your last name.')])
    email = StringField('Email', validators=[
        DataRequired('Please enter your email.'),
        Email('Please enter a valid email.'),
        validate_email])
    username = StringField('Username', validators=[
        DataRequired('Please enter a username.'),
        validate_username])
    password = PasswordField('Password', validators=[
        DataRequired('Please enter a password.'),
        Length(min=6, message='Passwords must have at least 6 characters.')])

    role_choices = [(0, 'Choose Role'),
                    (1, 'Administrator'),
                    (2, 'Unassigned'),
                    (3, 'Judge'),
                    (4, 'Singer'),
                    (5, 'Artist'),
                    (6, 'Mixer'),
                    (7, 'Animator')]

    role = SelectField('Role', coerce=int, choices=role_choices, validators=[
        DataRequired('Please choose a role.')])
    print(role)
    propic = FileField('Profile Picture (Optional)')
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    """
    WTForm for login page.
    """
    username = StringField('Username', validators=[DataRequired('Please enter your username.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password.')])
    submit = SubmitField('Sign in')

class CreateTeamForm(FlaskForm):
    """WTForm for creating a chorus battle team."""
    team_name = StringField('Name of Team', validators=[
        DataRequired('Please enter a name for your team.')])
    members = FieldList(StringField('Username'), min_entries=1, validators=[DataRequired('Please enter a member'), validate_username_exists])
    teampic = FileField('Team Logo (Optional)')
    submit = SubmitField('Create Team')

class CreateChorusBattleForm(FlaskForm):
    """
    WTForm for creating a chorus battle.
    """
    name = StringField('Name of Chorus Battle', validators=[
        DataRequired('Please enter a name for your chorus battle.')])
    description = TextAreaField('Description', validators=[
        DataRequired('Please provide a brief description of your chorus battle.')])
    # it would be nice if there was a stringfield for each separate rule
    # and the user is able to add a stringfield by clicking a button if more rules are needed
    rules = TextAreaField('List of Rules', validators=[
        DataRequired('Please provide a list of rules.')])
    prizes = TextAreaField('Prizes', validators=[
        DataRequired('Please provide a list of prizes that participants can win.')])
    video_link = StringField('Link to the Chorus Battle Introduction Video')
    no_of_rounds = StringField('Number of Rounds', validators=[
        DataRequired('Please enter the number of rounds.')])
    start_date = DateTimeField('Start Date/Time', default=datetime.now, format="%Y-%m-%dT%H:%M", validators=[DataRequired('Please enter a start date and time.')])
    submit = SubmitField('Create Chorus Battle')

class CreateRoundForm(FlaskForm):
    """WTForm for adding a round for a particular chorus battle."""
    # round_number = IntegerField('Round Number', validators=[
    #     DataRequired('Please enter the round number.')])
    theme = TextAreaField('Theme', validators=[
        DataRequired('Please enter the theme for this particular round.')])
    deadline = DateTimeField('Deadline', default=datetime.now, format="%Y-%m-%dT%H:%M", validators=[
        DataRequired('Please enter the deadline (date and time) for this round.')
        ])
    submit = SubmitField('Create New Round')

class CreateEntryForm(FlaskForm):
    """
    WTForm for adding an entry to a particular chorus battle.
    """
    team_name = StringField('Team Name', validators=[
        DataRequired('Please enter your team name')])
    title = StringField('Title', validators=[
        DataRequired('Please enter a title for your entry.')])
    description = TextAreaField('Description', validators=[
        DataRequired('Please provide of a description of your entry.')])
    video_link = StringField('Link to the Chorus Battle Video', validators=[
        DataRequired('Please provide a link to your Chorus Battle Video')])
    submit = SubmitField('Submit Entry')

class JudgeEntryForm(FlaskForm):
    """
    WTForm for a judge to grade a particular entry for a chorus battle.
    """

    # Each category will be graded on a scale of 1 to 10
    grades =   [(1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),
                (6, '6'),
                (7, '7'),
                (8, '8'),
                (9, '9'),
                (10, '10')]

    # The judges can select the scores for vocals, instrumental, art, editing, and transitions.
    vocals = SelectField('Vocals', coerce=int, choices=grades, validators=[
        DataRequired('Please select a score for the vocals.')])
    vocals_comment = TextAreaField()
    instrumental = SelectField('Instrumental', coerce=int, choices=grades, validators=[
        DataRequired('Please select a score for the instrumental.')])
    instrumental_comment = TextAreaField()
    art = SelectField('Art', coerce=int, choices=grades, validators=[
        DataRequired('Please select a score for the art.')])
    art_comment = TextAreaField()
    editing = SelectField('Editing', coerce=int, choices=grades, validators=[
        DataRequired('Please select a score for the editing.')])
    editing_comment = TextAreaField()
    transitions = SelectField('Vocals', coerce=int, choices=grades, validators=[
        DataRequired('Please select a score for the transitions.')])
    transitions_comment = TextAreaField()
    submit = SubmitField('Submit Entry')