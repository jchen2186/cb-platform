"""
This module contains the routes that allows flask to help navigate the
user to the templates.
"""

from flask import flash, render_template, request, session, redirect, url_for
from cbapp import app
from .forms import SignupForm, LoginForm, CreateChorusBattleForm, CreateEntryForm, CreateRoundForm
from .models import db, User, ChorusBattle, UserRole, Entry, Round
import urllib.parse
import os

# connect app to the postgresql database (local to our machines)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql://localhost/cbapp')
db.init_app(app)
app.secret_key = 'development-key'

@app.route('/', methods=['GET'])
def index():
    """The route '/' leads to the index page."""
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
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
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user is not None and user.check_password(password):
                session['username'] = form.username.data
                session['first_name'] = User.query.filter_by(username=username).first().firstname
                return redirect(url_for('home'))
            flash('Incorrect username or password.')
            return render_template('login.html', form=form) 
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/signup/', methods=['GET', 'POST'])
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
        session['role'] = newuser.role_id
        session['first_name'] = newuser.first_name
        return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/logout/')
def logout():
    """The route '/logout' will remove the user from the current session."""
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home/')
def home():
    """
    The route '/home' will redirect the user to the dashboard if the
    user is logged in. Otherwise, it will redirect the user to the login
    form in order to log in."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/chorusbattle/<cb>/', methods=['GET'])
def chorusInfo(cb=None):
    """
    The route '/chorusbattle/<cb> will direct the user to a page where the user
    can find more information about the selected chorus battle, stored
    as the variable cb.
    """
    row = ChorusBattle.query.filter_by(id=cb).first()

    if row:
        return render_template('chorusinfo.html', cb=row)

@app.route('/chorusbattle/<cb>/entries/', methods=['GET'])
def chorusEntries(cb=None):
    """
    The route '/chorusbattle/<cb>/entries' will direct the user to a page where
    they can view all the entries for the selected chorus battle.
    """
    entries = [{'title':'Title', 'owners':'Owners here', 'description':'Here will describe the entries'}]
    rounds = []
    rounds.append([{'title':'Blooming Light', 'owners':'Team Excite', \
        'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lobortis, nibh a vestibulum interdum, massa leo posuere libero, et elementum est magna in mi. Donec ligula lorem, pulvinar nec dapibus sit amet, consectetur vitae tortor. Proin venenatis augue dignissim, imperdiet tellus ac, maximus lacus. Etiam at urna risus. Donec bibendum nec elit at pharetra. Aenean hendrerit est vel eleifend pellentesque. Aenean at lacus iaculis, semper velit sed, sodales ex. \
        Cras facilisis nibh sed turpis vehicula, quis varius arcu consectetur. Quisque a nunc velit. Nulla dapibus mauris vel mauris mattis, aliquam interdum odio egestas. Suspendisse ullamcorper, metus eget mattis sollicitudin, ex erat condimentum leo, ut blandit magna sem bibendum dolor. Morbi quis semper nulla. Ut enim turpis, mollis ut eleifend eu, auctor vel urna. Quisque euismod est quis feugiat iaculis. Etiam in orci ante. Sed in elit volutpat, porta nulla euismod, molestie justo. Curabitur pulvinar, mauris et tincidunt ullamcorper, nulla eros congue risus, id vestibulum risus lacus interdum libero. Maecenas sodales sed arcu et suscipit. Nam sed sem id metus sollicitudin efficitur.', 'video':'https://www.youtube.com/embed/NxGvsfOEP20'},
        {'title':'Turn of the dawn', 'owners':'Team Raspberry', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lobortis, nibh a vestibulum interdum, massa leo posuere libero, et elementum est magna in mi. Donec ligula lorem, pulvinar nec dapibus sit amet, consectetur vitae tortor. Proin venenatis augue dignissim, imperdiet tellus ac, maximus lacus. Etiam at urna risus. Donec bibendum nec elit at pharetra. Aenean hendrerit est vel eleifend pellentesque. Aenean at lacus iaculis, semper velit sed, sodales ex. \
        Cras facilisis nibh sed turpis vehicula, quis varius arcu consectetur. Quisque a nunc velit. Nulla dapibus mauris vel mauris mattis, aliquam interdum odio egestas. Suspendisse ullamcorper, metus eget mattis sollicitudin, ex erat condimentum leo, ut blandit magna sem bibendum dolor. Morbi quis semper nulla. Ut enim turpis, mollis ut eleifend eu, auctor vel urna. Quisque euismod est quis feugiat iaculis. Etiam in orci ante. Sed in elit volutpat, porta nulla euismod, molestie justo. Curabitur pulvinar, mauris et tincidunt ullamcorper, nulla eros congue risus, id vestibulum risus lacus interdum libero. Maecenas sodales sed arcu et suscipit. Nam sed sem id metus sollicitudin efficitur.', 'video':'https://www.youtube.com/embed/dQw4w9WgXcQ'}])
    rounds.append([{'title':'Entry 1', 'owners':'Team 2', 'description':'Here will describe the entries for round 2. There will be fewer teams here due to elimination. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam lobortis, nibh a vestibulum interdum, massa leo posuere libero, et elementum est magna in mi. Donec ligula lorem, pulvinar nec dapibus sit amet, consectetur vitae tortor. Proin venenatis augue dignissim, imperdiet tellus ac, maximus lacus. Etiam at urna risus. Donec bibendum nec elit at pharetra. Aenean hendrerit est vel eleifend pellentesque. Aenean at lacus iaculis, semper velit sed, sodales ex.', 'video':'https://www.youtube.com/embed/G2lXOwRi7Tk'}])
    print(rounds)
    return render_template('entries.html', cb=cb, rounds=rounds)

@app.route('/chorusbattle/<cb>/entries/<rd>/create/', methods=['GET', 'POST'])
def createEntry(cb=None, rd=None):
    """
    The route '/chorusbattle/<cb>/entries' will direct a participant to a page where
    they can create a new entry for the newest round in the selected chorus battle.
    """
    form = CreateEntryForm()
    if request.method == 'POST':
        if not form.validate():
            # we need to update the entries table on postgres
            return render_template('createentry.html', cb=cb, rd=rd, form=form)
        newEntry = Entry(form.team_name.data, form.description.data,
            form.video_link.data, cb, rd)

        db.session.add(newEntry)
        db.session.commit()

        return redirect(url_for('chorusBattle', cb=cb))

    elif request.method == 'GET':
        return render_template('createentry.html', cb=cb, rd=rd, form=form)

@app.route('/team/<name>', methods=['GET'])
def team(name=None):
    """
    The route '/team/<name>' will direct the user to a page containing
    information about the selected chorus battle team, stored as the
    variable name.
    """
    return render_template('team.html')

@app.route('/chorusbattle/', methods=['GET'])
def chorusBattleAll():
    chorusBattles = ChorusBattle.query.all()
    info = []

    for cb in chorusBattles:
        info.append({'name': cb.name,
                     'description': cb.description,
                     'link': urllib.parse.quote('/chorusbattle/' + str(cb.id))})


    return render_template("chorusbattles.html", info=info)

@app.route('/create/chorusbattle/', methods=['GET', 'POST'])
def createChorusBattle():
    """
    The route '/create/chorusbattle' will direct the user, who has 
    to be a Judge, to the form where he/she will fill out information
    relating to the chorus battle.
    After submitting the form, the user will be notified of any errors,
    if there are any. Otherwise, the chorus battle will be created.
    """
    form = CreateChorusBattleForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('createchorusbattle.html', form=form)
        newcb = ChorusBattle(form.name.data, form.description.data,
            form.rules.data, form.prizes.data, form.video_link.data)

        db.session.add(newcb)
        db.session.commit()

        return redirect(url_for('chorusInfo', cb_id=newcb.id,cb=form.name.data))

    elif request.method == 'GET':
        return render_template('createchorusbattle.html', form=form)

@app.route('/chorusbattle/<cb>/judge/<entry>', methods=['GET', 'POST'])
def judgeEntry(cb=None,entry=None):
    if request.method == 'GET':
        return render_template("judgingtool.html", chorusBattle=cb, entry=entry)

@app.route('/create/round/', methods=['GET', 'POST'])
def createRound():
    """
    The route '/create/round' will direct the user, who has to be a Judge,
    to the form where he/she will fill out information in order to add a round
    to the chorus battle he/she is hosting.
    After submitting the form, the user will be notified of any errors, if
    there are any. Otherwise, the round will be created.
    """
    form = CreateRoundForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('createround.html', form=form)

        newRound = Round(form.round_number.data, form.theme.data, form.deadline.data)
        db.session.add(newRound)
        db.session.commit()

        # somehow redirect the user back to the chorus battle info page for
        # this particular chorus battle
        return redirect(url_for('/chorusbattle/'))

    elif request.method == 'GET':
        return render_template('createround.html', form=form)


# work in progress
@app.route('/user/<username>/', methods=['GET'])
def getUserProfile(username=None):
    """
    The route '/user/<username>' directs the user to the profile page of
    the user with the specified username.
    """
    row = User.query.filter_by(username=username).first()

    if row:
        return render_template("userprofile.html", username=row.get_username(), role=row.get_role())

@app.route('/help/faq/', methods=['GET'])
def faq():
    """
    The route '/help/faq/' directs the user to the Frequently Asked Questions
    page. This page contains the user documentation which will assist the
    end users who are using the app.
    """
    return render_template("faq.html")
