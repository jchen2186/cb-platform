"""
models.py
Contains classes for the objects that connect to our Postgres database.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import generate_password_hash, check_password_hash
from flask import session

db = SQLAlchemy()

judges = db.Table('judges', 
    db.Column('user_id', db.Integer,db.ForeignKey('users.id'), nullable=False),
    db.Column('chorusbattle_id', db.Integer, db.ForeignKey('chorusbattles.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'chorusbattle_id'))
"""
Association table showing organizers for chorus battles)
"""

chorusbattle_entries = db.Table('chorusbattle_entries', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('entry_id', db.Integer, db.ForeignKey('entries.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'entry_id'))
"""
Association table showing chorus battlers for each entry
"""

user_teams = db.Table('user_teams', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), nullable=False),
    db.Column('member_status', db.String(100), default='pending'), # Status: ['pending', 'member']
    db.PrimaryKeyConstraint('user_id', 'team_id'))
"""
Association table showing users on a particular team
"""

subscriptions = db.Table('subscriptions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('chorusbattle_id', db.Integer, db.ForeignKey('chorusbattles.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id','chorusbattle_id'))
"""
Association table showing chorus battle that users are subscribed to to show notifications.
"""

class Notification(db.Model):
    """
    Class to store notifications made by user.
    """
    __tablename__='notifications'
    id = db.Column(db.Integer, primary_key= True)
    notifier = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    chorusbattle_id = db.Column(db.Integer, db.ForeignKey('chorusbattles.id'), nullable=False)
    message = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, notifier, chorusbattle_id, message):
        self.notifier=notifier
        self.chorusbattle_id=chorusbattle_id
        self.message=message

class User(db.Model):
    """
    Chorus battle user class. This table stores the users in the system, and the user's information.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True) #: Primary key to identify the user
    firstname = db.Column(db.String(100)) #: First name of the user.
    lastname = db.Column(db.String(100)) #: Last name of the user.
    email = db.Column(db.String(120), unique=True) #: Email of the user.
    password_hash = db.Column(db.String(100)) #: Password for the user, stored as a hashed value.
    username = db.Column(db.String(100), unique=True) #: Unique username for the user.
    role_id = db.Column(db.Integer, db.ForeignKey('userroles.id')) #: User role for the user.
    user_icon = db.Column(db.LargeBinary) #: Icon for the user.
    description = db.Column(db.String(500), default="No description yet!") # Description for the user.
    current_status = db.Column(db.String(500), default="No current status!") # Current Status for the user.
    chorusbattles = db.relationship('ChorusBattle', secondary=judges, backref='users') #: A history of all the chorus btatles the user has participated in.
    entries = db.relationship('Entry', secondary=chorusbattle_entries, backref='users') #: All the entries the user has worked on.
    teams = db.relationship('Team', secondary=user_teams, backref='users') #: All the teams the users have joined.
    subscriptions = db.relationship('ChorusBattle', secondary=subscriptions, backref='subscriber')

    def __init__(self, firstname, lastname, email, password, username, role_id, user_icon):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password) # encrypt password with salted hash
        self.username = username
        self.role_id = role_id
        self.user_icon = user_icon
  
    def set_password(self, password):
        """
        Sets password by converting plain text password to hashed password

        Args:
            password (str): new password to replace current password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if password matches hashed password

        Args:
          password (str): password to be checked

        Returns:
          bool: True if password matches hashed password and false if not
        """
        return check_password_hash(self.password_hash,password)

    def get_username(self):
        """
        Get the user's username.
        """
        return self.username

    def get_role(self):
        """
        Gets the user's role (in words).
        """
        role = self.role_id

        roles = ['Admin', 'Unassigned', 'Judge', 'Singer', 'Artist', 'Mixer', 'Animator']
        return roles[role - 1]

    def get_icon(self):
        return self.user_icon

    @staticmethod
    def is_username_unique(username):
        """
        Checks whether username is unique

        Args:
          username (str): username to be checked

        Returns:
          bool: True if username is unique and False if it is not 
        """
        if db.session.query(User.id).filter(User.username==username).count() > 0:
            return False
        return True

    @staticmethod
    def is_email_unique(email):
        """
        Checks whether email is unique

        Args:
          email (str): email to be checked

        Returns:
          bool: True if email is unique and False if it is not 
        """
        if db.session.query(User.id).filter(User.email==email).count() > 0:
            return False
        return True

class ChorusBattle(db.Model):
    """
    Model to store chorus battle and related information.
    """
    __tablename__ = 'chorusbattles'
    id = db.Column(db.Integer, primary_key = True) #: Primary key to identify the chorus battle.
    name = db.Column(db.String(150)) #: Name of the chorus battle.
    description = db.Column(db.String(500)) #: User-inputted description for the chorus battle.
    rules = db.Column(db.String(500)) #: User-inputted rules for the chorus battle.
    prizes = db.Column(db.String(500)) #: Prizes for the chorus battle.
    video_link = db.Column(db.String(150)) #: Allows for a link to a video about the chorus battle.
    no_of_rounds = db.Column(db.Integer)
    start_date = db.Column(db.DateTime(timezone=False), default=func.now())
    creator_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    entries = db.relationship('Entry') #: Available entries in the chorus battle.
    teams = db.relationship('Team') #: Teams involved in this chorus battle.
    rounds = db.relationship('Round') #: Rounds in the chorus battle.
    # judges = db.relationship('Judge', secondary=judges)
    subscribers = db.relationship("User", secondary='subscriptions', backref="subbed_cbs")

    def __init__(self, name, description, rules, prizes, video_link, start_date, no_of_rounds, creator_id):
        self.name = name
        self.description = description
        self.rules = rules
        self.prizes = prizes
        self.video_link = video_link
        self.start_date = start_date
        self.no_of_rounds = no_of_rounds
        self.creator_id = creator_id

    def change_name(self, newName):
        """
        Allows users to change the name of the chorus battle.

        Args:
            newName(str: the new name to replace the old name
        """
        self.name = newName
    
    def addDescription(self, description):
        """
        Allows the the user to add a description to the chorus battle.

        Args:
            description(str): the description provided
        """
        self.description = description


        
class UserRole(db.Model):
    """
    Model to store the roles and the associated id with the role.
    
    0.Choose Role
    1. Administrator
    2. Unassigned
    3. Judge
    4. Singer
    5. Artist
    6. Mixer
    7. Animator
    """
    __tablename__ = 'userroles'
    id = db.Column(db.Integer, primary_key = True) #: The corresponding id to the role.
    role_title = db.Column(db.String(100)) #: Name of the role.

    def __init__(self, role_id, role_title):
        self.id = role_id
        self.role_title = role_title

class Entry(db.Model):
    """
    Model to store the entries of chorus battles. Entries come with a video and descrpition.
    """
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key = True) #: Primary key to identify the round.

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id')) #: id of the team that made the entry.
    title = db.Column(db.String(100)) #: Title of the entry.
    description = db.Column(db.String(500)) #: User-inputted description of the entry.
    video_link= db.Column(db.String(500)) #: Link to the video entry, preferably YouTube so we can embed it.
    submission_date = db.Column(db.DateTime(timezone=True), default=func.now()) #: Date of the submission of the entry.
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id')) #: The chorus battle the entry belongs to
    round_number = db.Column(db.Integer, db.ForeignKey('rounds.id')) #: The round of the chorus battle that the entry belongs to.

    def __init__(self, team_name, title, description, video_link, chorusid, round_number):
        self.team_id = Team.query.filter_by(team_name=team_name).first().id
        self.title = title
        self.description = description
        self.video_link = video_link
        self.chorusbattle = chorusid
        self.round_number = round_number

class Round(db.Model):
    """ 
    Model to store the rounds of a chorus battle. It contains information about the round.
    """
    __tablename__ = 'rounds'
    id = db.Column(db.Integer, primary_key = True) #: Primary key to identify the round. 
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id')) #: The chorus battle the round belongs to.
    theme = db.Column(db.String(500)) #: User-inputted theme for the round of the chorus battle.
    deadline = db.Column(db.DateTime(timezone=True)) #: Deadline for the submissions of the round.
    round_number = db.Column(db.Integer) #: Round number to show the progression of the chorus battle. Why is this needed?

    def __init__(self, chorusbattle, theme, deadline):
        self.chorusbattle = chorusbattle
        self.theme = theme
        self.deadline = deadline
        self.round_number = session.query(Round.round_number).filter_by(chorusbattle=chorusbattle).count() + 1

class Team(db.Model):
    """
    Model to store the team members and team name.
    """
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key = True) #: Primary key to identify the team.
    team_name = db.Column(db.String(100)) #: Name of the team.
    leader_id = db.Column(db.String(100), db.ForeignKey('users.id')) #: User ID of team leader.
    team_logo = db.Column(db.LargeBinary) #: Image for the team logo.
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id')) #: The chorus battle the team is participating in.
    member = db.relationship('User', secondary='user_teams') #: Team members of the team
    """ id of the ChorusBattle the team belongs to. A new team must be created per chorus battle, even if they have the same name and same members.
    """

    def __init__(self, team_name, leader_id, team_logo, chorusbattle):
        self.team_name = team_name
        self.leader_id = leader_id
        self.team_logo = team_logo
        self.chorusbattle = chorusbattle


class Judge(db.Model):
    """
    Model to store user_id of judges to the respective chorus battle. Uses association table judges.
    """
    __tablename__ = 'judges',
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    chorusbattle_id = db.Column(db.Integer, db.ForeignKey('chorusbattles.id'), primary_key = True)

    def __init__(self, user_id, chorusbattle_id):
        self.user_id = user_id
        self.chorusbattle_id = chorusbattle_id
