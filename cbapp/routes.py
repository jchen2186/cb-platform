"""
This module contains the routes that allows flask to help navigate the
user to the templates.
"""

from flask import render_template, request, session, redirect, url_for
from cbapp import app
from .forms import SignupForm, LoginForm
from .models import db, User, ChorusBattle, UserRole, Entry
from cbapp import app
import os

# connect app to the postgresql database (local to our machines)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql://localhost/cbapp')
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

@app.route('/chorusbattle/<cb>', methods=['GET'])
def chorusInfo(cb=None):
    """
    The route '/chorusbattle/<cb> will direct the user to a page where the user
    can find more information about the selected chorus battle, stored
    as the variable cb.
    """
    return render_template('chorusinfo.html', chorusTitle=cb)

@app.route('/chorusinfo/<cb>/entries', methods=['GET'])
def chorusEntries(cb=None):
    """
    The route '/chorusinfo/<cb>/entries' will direct the user to a page where
    they can view all the entries for the selected chorus battle.
    """
    entries = [{'title':'Title', 'owners':'Owners here', 'description':'Here will describe the entries'}]
    rounds = []
    rounds.append([{'title':'Entry 1', 'owners':'Team 1', \
        'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lobortis, nibh a vestibulum interdum, massa leo posuere libero, et elementum est magna in mi. Donec ligula lorem, pulvinar nec dapibus sit amet, consectetur vitae tortor. Proin venenatis augue dignissim, imperdiet tellus ac, maximus lacus. Etiam at urna risus. Donec bibendum nec elit at pharetra. Aenean hendrerit est vel eleifend pellentesque. Aenean at lacus iaculis, semper velit sed, sodales ex. \
        Cras facilisis nibh sed turpis vehicula, quis varius arcu consectetur. Quisque a nunc velit. Nulla dapibus mauris vel mauris mattis, aliquam interdum odio egestas. Suspendisse ullamcorper, metus eget mattis sollicitudin, ex erat condimentum leo, ut blandit magna sem bibendum dolor. Morbi quis semper nulla. Ut enim turpis, mollis ut eleifend eu, auctor vel urna. Quisque euismod est quis feugiat iaculis. Etiam in orci ante. Sed in elit volutpat, porta nulla euismod, molestie justo. Curabitur pulvinar, mauris et tincidunt ullamcorper, nulla eros congue risus, id vestibulum risus lacus interdum libero. Maecenas sodales sed arcu et suscipit. Nam sed sem id metus sollicitudin efficitur.', 'video':'https://www.youtube.com/embed/NxGvsfOEP20'},
        {'title':'Entry 2', 'owners':'Team 2', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lobortis, nibh a vestibulum interdum, massa leo posuere libero, et elementum est magna in mi. Donec ligula lorem, pulvinar nec dapibus sit amet, consectetur vitae tortor. Proin venenatis augue dignissim, imperdiet tellus ac, maximus lacus. Etiam at urna risus. Donec bibendum nec elit at pharetra. Aenean hendrerit est vel eleifend pellentesque. Aenean at lacus iaculis, semper velit sed, sodales ex. \
        Cras facilisis nibh sed turpis vehicula, quis varius arcu consectetur. Quisque a nunc velit. Nulla dapibus mauris vel mauris mattis, aliquam interdum odio egestas. Suspendisse ullamcorper, metus eget mattis sollicitudin, ex erat condimentum leo, ut blandit magna sem bibendum dolor. Morbi quis semper nulla. Ut enim turpis, mollis ut eleifend eu, auctor vel urna. Quisque euismod est quis feugiat iaculis. Etiam in orci ante. Sed in elit volutpat, porta nulla euismod, molestie justo. Curabitur pulvinar, mauris et tincidunt ullamcorper, nulla eros congue risus, id vestibulum risus lacus interdum libero. Maecenas sodales sed arcu et suscipit. Nam sed sem id metus sollicitudin efficitur.', 'video':'https://www.youtube.com/embed/dQw4w9WgXcQ'}])
    rounds.append([{'title':'Entry 1', 'owners':'Team 2', 'description':'Here will describe the entries for round 2. There will be fewer teams here due to elimination. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lobortis, nibh a vestibulum interdum, massa leo posuere libero, et elementum est magna in mi. Donec ligula lorem, pulvinar nec dapibus sit amet, consectetur vitae tortor. Proin venenatis augue dignissim, imperdiet tellus ac, maximus lacus. Etiam at urna risus. Donec bibendum nec elit at pharetra. Aenean hendrerit est vel eleifend pellentesque. Aenean at lacus iaculis, semper velit sed, sodales ex.', 'video':'https://www.youtube.com/embed/G2lXOwRi7Tk'}])
    print(rounds)
    return render_template('entries.html', chorusTitle=cb, rounds=rounds)

@app.route('/team/<name>', methods=['GET'])
def team(name=None):
    """
    The route '/team/<name>' will direct the user to a page containing
    information about the selected chorus battle team, stored as the
    variable name.
    """
    return render_template('team.html')

@app.route('/chorusbattle', methods=['GET'])
def chorusBattleAll():
    return render_template("chorusbattles.html")

@app.route('/chorusbattle/<cbname>', methods=['GET'])
def chorusBattle(cbname=None):
    return render_template("tournament.html", cbname=cbname)
