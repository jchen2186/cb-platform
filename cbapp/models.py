from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import generate_password_hash, check_password_hash

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
    db.PrimaryKeyConstraint('user_id', 'team_id'))
"""
Association table showing users on a particular team
"""

class User(db.Model):
    """
    Chorus battle user class. This table stores the users in the system, and the user's information.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('userroles.id'))
    user_icon = db.Column(db.LargeBinary())
    chorusbattles = db.relationship('ChorusBattle', secondary=judges, backref='users')
    entries = db.relationship('Entry', secondary=chorusbattle_entries, backref='users')
    teams = db.relationship('Team', secondary=user_teams, backref='users')
    
    def __init__(self, firstname, lastname, email, password, username, role_id):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password) # encrypt password with salted hash
        self.username = username
        self.role_id = role_id
  
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

class ChorusBattle(db.Model):
    """
    Chorus battle class
    """
    __tablename__ = 'chorusbattles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(500))
    rules = db.Column(db.String(500))
    prizes = db.Column(db.String(500))
    video_link = db.Column(db.String(150))
    entries = db.relationship('Entry')
    teams = db.relationship('Team')
    # judges = db.relationship('Judge', secondary=judges)

    def __init__(self, name, description, rules, prizes, video_link):
        self.name = name
        self.description = description
        self.rules = rules
        self.prizes = prizes
        self.video_link = video_link

    def change_name(self, newName):
        self.name = newName
    
    def addDescription(self, description):
        self.description = description
        
class UserRole(db.Model):
    """
    User role class
    """
    __tablename__ = 'userroles'
    id = db.Column(db.Integer, primary_key = True)
    role_title = db.Column(db.String(100))

    def __init__(self, role_id, role_title):
        self.id = role_id
        self.role_title = role_title

class Entry(db.Model):
    """
    Model to store the entries of chorus
    """
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key = True) #: Primary key to identify the round.

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id')) #: id of the team that made the entry.
    description = db.Column(db.String(500)) #: User-inputted description of the entry.
    video_link= db.Column(db.String(500)) #: Link to the video entry, preferably YouTube so we can embed it.
    submission_date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id'))
    round_number = db.Column(db.Integer, db.ForeignKey('rounds.id'))

    def __init__(self, team_name, description, video_link, chorusname, round_number):
        self.team_name = team_name
        self.description = description
        self.video_link = video_link
        chorusid = ChorusBattle.query.filter_by(name=chorusname).first().getID()
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

    def __init__(self, chorusbattle, deadline, round_number):
        self.chorusbattle = chorusbattle
        self.deadline = deadline
        self.round_number = round_number

class Team(db.Model):
    """
    Model to store the team members and team name.
    """
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key = True) #: Primary key to identify the team.
    team_name=db.Column(db.String(100)) #: Name of the team.
    team_logo = db.Column(db.LargeBinary()) #: Image for the team logo.
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id')) 
    """ id of the ChorusBattle the team belongs to. A new team must be created per chorus battle, even if they have the same name and same members.
    """

    def __init__(self, id, chorusbattle):
        self.id = id
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
