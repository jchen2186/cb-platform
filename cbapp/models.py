from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
  """
  Chorus battle user class
  """
  __tablename__ = 'users'
  user_id = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  password_hash = db.Column(db.String(54))
  username = db.Column(db.String(100))
  role = db.Column(db.String(100), foreign_key = True)


  def __init__(self, firstname, lastname, email, password,username):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password) # encrypt password with salted hash
    self.username = username

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
    cb_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))

class UserRole(db.Model):
  """
  User role class
  """
  __tablename__ = 'userroles'
  role_id = db.Column(db.Integer, primary_key = True)
  role_title = db.Column(db.String(50))
