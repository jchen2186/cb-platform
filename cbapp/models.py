from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

"""
Association table showing organizers for chorus battles)
"""
judges = db.Table('judges', 
    db.Column('user_id', db.Integer,db.ForeignKey('users.id'), nullable=False),
    db.Column('chorusbattle_id', db.Integer, db.ForeignKey('chorusbattles.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'chorusbattle_id'))

"""
Association table showing chorus battlers for each entry
"""
chorusbattle_entries = db.Table('chorusbattle_entries', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('entry_id', db.Integer, db.ForeignKey('entries.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'entry_id'))

"""
Association table showing users on a particular team
"""
user_teams = db.Table('user_teams', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'team_id'))

class User(db.Model):
    """
    Chorus battle user class
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('userroles.id'))
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

    def changeName(self, newName):
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
    Chorus battle Entry class
    """
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key = True)
    submission_date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id'))

    def __init__(self, id, submission_date, chorusbattle):
        self.id = id
        self.submission_date = submission_date
        self.chorusbattle = chorusbattle

class Round(db.Model):
    """ 
    Chorus Battle Round class
    """
    __tablename__ = 'rounds'
    id = db.Column(db.Integer, primary_key = True)
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id'))
    theme = db.Column(db.String(500))
    deadline = db.Column(db.DateTime(timezone=True))

    def __init__(self, chorusbattle, deadline):
        self.chorusbattle = chorusbattle
        self.deadline = deadline

class Team(db.Model):
    """
    Chorus Battle Team class
    """
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key = True)
    chorusbattle = db.Column(db.Integer, db.ForeignKey('chorusbattles.id'))

    def __init__(self, id, chorusbattle):
        self.id = id
        self.chorusbattle = chorusbattle

class Judge(db.Model):
    __tablename__ = 'judges',
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    chorusbattle_id = db.Column(db.Integer, db.ForeignKey('chorusbattles.id'), primary_key = True)

    def __init__(self, user_id, chorusbattle_id):
        self.user_id = user_id
        self.chorusbattle_id = chorusbattle_id

# class Chorus_Battle_Entry(db.Model):
#     __tablename__ = 'chorusbattle_entries'
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
#     entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'), primary_key = True)

#     def __init__(self, user_id, entry_id):
#         self.user_id = user_id
#         self.entry_id = entry_id

# class User_Team(db.Model):
#      __tablename__ = 'user_teams'
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
#     team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key = True)

#     def __init__(self, user_id, team_id):
#         self.user_id = user_id
#         self.team_id = team_id

