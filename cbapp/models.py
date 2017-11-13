from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

"""
Association Table for User and Chorus Battles (Many to many relationship)
"""
organizers = db.Table(
    'organizers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('chorusbattle_id', db.Integer, db.ForeignKey('chorusbattles.id'))
)


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
    chorusbattles = db.relationship('ChorusBattle', secondary=user_chorusbattles)
    # role = db.Column(db.Integer, db.ForeignKey('userroles.id'))

    def __init__(self, firstname, lastname, email, password, username, role):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password) # encrypt password with salted hash
        self.username = username
        self.role = role
  
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


class ChorusBattle(db.Model):
    """
    Chorus battle class
    """
    __tablename__ = 'chorusbattles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    entries = db.relationship('Entry')

    def __init__(self,title):
        self.name = name

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
    Chorus battle entry
    """
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key = True)
    submission_date = db.Column(db.Date) 
    owners = db.relationship('User')
    chorusbattle = db.Column(db.Integer)


class Round(db.Model):
    """ 
    Chorus Battle Rounds
    """
    __tablename__ = 'rounds'
    id = db.Column(db.Integer, primary_key = True)

class Team(db.Model):
    """
    Information for a team of a chorus battle
    """
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key = True)

