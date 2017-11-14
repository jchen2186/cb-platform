"""
This module contains the routes that allows flask to help navigate the
user to the templates.
"""

from flask import render_template, request, session, redirect, url_for
from cbapp import app
from .forms import SignupForm, LoginForm
from .models import db, User #, ChorusBattle, UserRole, Entry

# connect app to the postgresql database (local to our machines)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cbapp'
db.init_app(app)
app.secret_key = 'development-key'

@app.route('/', methods=['GET'])
def index():
    """The route '/' leads to the index page."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    The route '/login' leads to the login form if the user is not already
    logged in. When the user submits the form, this function will verify
    whether or not the login credentials are valid and handle the cases
    accordingly.
    If the user is logged in, he/she gets redirected to the
    route '/home' and will not see the login form.
    """
    if 'username' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            session['username'] = form.username.data
            return redirect(url_for('home'))

        return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    The route '/signup' leads to the signup form if the user is not already
    logged in. When the user submits the form, this function will verify that
    the form is filled out properly. It will then add the user to the database
    and sessions.
    """
    if 'username' in session:
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)

        newuser = User(form.first_name.data, form.last_name.data, form.email.data,
                       form.password.data, form.username.data, form.role.data)
        db.session.add(newuser)
        db.session.commit()

        session['username'] = newuser.username
        return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    """The route '/logout' will remove the user from the current session."""
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    """
    The route '/home' will redirect the user to the dashboard if the
    user is logged in. Otherwise, it will redirect the user to the login
    form in order to log in."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/chorusinfo/<cb>', methods=['GET'])
def chorusInfo(cb=None):
    """
    The route '/chorusinfo/<cb> will direct the user to a page where the user
    can find more information about the selected chorus battle, stored
    as the variable cb.
    """
    return render_template('chorusinfo.html', chorusTitle=cb)

@app.route('/chorusinfo/<cb>/entries', methods=['GET'])
def chorusEntries(cb=None):
	entries = [{'title':'Title', 'owners':'Owners here', 'description':'Here will describe the entries'}]
	return render_template('entries.html', entries=entries)

@app.route('/team/<name>', methods=['GET'])
def team(name=None):
    """
    The route '/team/<name>' will direct the user to a page containing
    information about the selected chorus battle team, stored as the
    variable name.
    """
    return render_template('team.html')
