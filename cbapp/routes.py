"""
routes.py
This module contains the routes that allows flask to help navigate the
user to the templates.
"""

from flask import flash, render_template, request, session, redirect, url_for
from cbapp import app
from .forms import SignupForm, LoginForm, CreateChorusBattleForm, CreateEntryForm, CreateRoundForm, CreateTeamForm, InviteTeamForm
from .models import db, User, ChorusBattle, UserRole, Entry, Round, Team, user_teams
import urllib.parse
import os
from base64 import b64encode
import copy

# pylint: disable=C0103

# connect app to the postgresql database (local to our machines)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgresql://localhost/cbapp')
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
                user = User.query.filter_by(username=username).first()
                session['role'] = user.get_role()
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
        propic = None
        if form.propic.data:
            propic = request.files.getlist('propic')[0].read()

        newuser = User(form.first_name.data, form.last_name.data, form.email.data,
                       form.password.data, form.username.data, form.role.data, propic)
        db.session.add(newuser)
        db.session.commit()
        print(newuser)
        session['username'] = newuser.username
        session['role'] = newuser.role_id
        session['first_name'] = newuser.firstname
        return redirect(url_for('home'))
        # return render_template('home.html', propic=b64encode(propic).decode('utf-8'))

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
    print(session.items())
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', icon=getUserIcon((session['username'] if 'username' in session else None)))

@app.route('/chorusbattle/<cb>/', methods=['GET'])
def chorusInfo(cb=None):
    """
    The route '/chorusbattle/<cb> will direct the user to a page where the user
    can find more information about the selected chorus battle, stored
    as the variable cb.
    """
    row = ChorusBattle.query.filter_by(id=cb).first()

    if row:
        return render_template('chorusinfo.html', cb=row, icon=getUserIcon((session['username'] if 'username' in session else None)))

@app.route('/chorusbattle/<cb>/entries/', methods=['GET'])
def chorusEntries(cb=None):
    """
    The route '/chorusbattle/<cb>/entries' will direct the user to a page where
    they can view all the entries for the selected chorus battle.
    """
    row = ChorusBattle.query.filter_by(id=cb).first()
    rounds = []
    currRound = []
    maxRound = row.no_of_rounds
    roundCount = len(Round.query.filter_by(chorusbattle=cb).all())
    print('roundCount', roundCount)
    for rd in range(1, roundCount+1):
        roundQuery = Round.query.filter_by(chorusbattle=cb, round_number=rd).first()
        theme = roundQuery.theme
        deadline = roundQuery.deadline
        currRound.append(theme)
        currRound.append(deadline)

        entries = Entry.query.filter_by(chorusbattle=cb, round_number=rd).all()
        for entry in entries:
            currRound.append({'title':entry.title, 'owners':Team.query.filter_by(id=entry.team_id).first().team_name, 'description':entry.description, 'video_link':entry.video_link})
        rounds.append(currRound)
    
    return render_template('entries.html', cb=row, maxRound=maxRound, roundCount=roundCount, rounds=rounds, icon=getUserIcon((session['username'] if 'username' in session else None)))

@app.route('/chorusbattle/<cb>/entries/create/', methods=['GET', 'POST'])
def createEntry(cb=None):
    """
    The route '/chorusbattle/<cb>/entries' will direct a participant to a page where
    they can create a new entry for the newest round in the selected chorus battle.
    """
    form = CreateEntryForm()
    rd = len(Round.query.filter_by(chorusbattle=cb).all())
    if request.method == 'POST':
        if not form.validate():
            # we need to update the entries table on postgres
            return render_template('createentry.html', cb=cb, rd=rd, form=form, icon=getUserIcon((session['username'] if 'username' in session else None)))
        newEntry = Entry(form.team_name.data, form.title.data, form.description.data,
                         form.video_link.data, cb, rd)

        db.session.add(newEntry)
        db.session.commit()

        return redirect(url_for('chorusEntries', cb=newEntry.chorusbattle))

    elif request.method == 'GET':
        return render_template('createentry.html', cb=cb, rd=rd, form=form, icon=getUserIcon((session['username'] if 'username' in session else None)))

@app.route('/team/<teamID>/', methods=['GET'])
def team(teamID=None):
    """
    The route '/team/<name>' will direct the user to a page containing
    information about the selected chorus battle team, stored as the
    variable name.
    """
    form = InviteTeamForm()
    team = Team.query.filter_by(id=teamID).first()
    team_users = db.session.query(user_teams).filter_by(team_id=teamID, member_status='member').all()
    team_members = []
    for member in team_users:
        userObject = {
            'user': copy.deepcopy(User.query.filter_by(id=member.user_id).first())
        }
        userObject['role'] = UserRole.query.filter_by(id=userObject['user'].role_id).first().role_title.capitalize()
        userObject['user_icon'] = b64encode(userObject['user'].user_icon).decode('utf-8')
        team_members.append(userObject)
    if team:
        return render_template('team.html', form=form, team=team, team_members=team_members, icon=getUserIcon((session['username'] if 'username' in session else None)))
    return redirect(request.referrer or url_for('home'))

@app.route('/chorusbattle/<cb>/createteam/', methods=['GET', 'POST'])
def createTeam(cb=None):
    """
    The route '/create/team/' will direct the user to a form that
     will allow them to create a team
    """
    form = CreateTeamForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template ('createteam.html', form=form, cb=cb, icon=getUserIcon((session['username'] if 'username' in session else None)))
        teampic = None
        if form.teampic.data:
            teampic = request.files.getlist('teampic')[0].read()
        leader_id = User.query.filter_by(username=session['username']).first().id
        print(form.members, '\n',form.members.entries,'\n',  form.members.data)
        newteam = Team(form.team_name.data, leader_id, teampic, cb)
        db.session.add(newteam)
        db.session.commit()

        return redirect(url_for('team', name=form.team_name.data))

    elif request.method == 'GET':
        return render_template("createteam.html", form=form, cb=cb, icon=getUserIcon((session['username'] if 'username' in session else None)))

@app.route('/team/<teamID>/invite/', methods=['GET', 'POST'])
def inviteTeam(teamID=None):
    """
    The route /team/<teamID>/invite/ allows a team leader to invite a user to their team
    """
    form = InviteTeamForm()
    if request.method == 'POST':
        team = Team.query.filter_by(id=teamID).first()
        invitee = User.query.filter_by(username=form.username.data).first()
        if invitee:
            team_user = db.session.query(user_teams).filter_by(user_id=invitee.id, team_id=teamID).first()
            if team_user:
                flash('You have already invited ' + invitee.username +'.')
            else:
                team.member.append(invitee)
                db.session.commit()
                flash('You have invited ' + invitee.username + '.')
        else:
            flash(form.username.data + 'is not a registered user.')
    return redirect(request.referrer or url_for('team', teamID=teamID))

@app.route('/team/<teamID>/join/', methods=['GET'])
def joinTeam(teamID=None):
    """
    The route /team/<teamID>/join/ allows users to accept an invitation to join a team.
    """
    userID = User.query.filter_by(username=session['username']).first().id
    team_user = db.session.query(user_teams).filter_by(user_id=userID, team_id=teamID).first()
    team_name = Team.query.filter_by(id=teamID).first().team_name
    if team_user:
        if team_user.member_status == 'member':
            flash('You are a member of ' + team_name + ' already.')
            return redirect(request.referrer or url_for('home'))
        db.engine.execute("UPDATE user_teams " + \
            "SET member_status = 'member'" + \
            "WHERE user_id=" + userID + " and team_id=" + teamID + ";")
        flash('You have successfully joined ' + team_name + '.')
    else:
        flash('You are not invited to ' + team_name + '.')
    return redirect(request.referrer or url_for('home'))

@app.route('/chorusbattle/', methods=['GET'])
def chorusBattleAll():
    """
    The route /chorusbattle/ directs the user to a page that displays
    all chorus battles.
    """
    chorusBattles = ChorusBattle.query.all()
    info = []

    for cb in chorusBattles:
        info.append({'name': cb.name,
                     'description': cb.description,
                     'link': urllib.parse.quote('/chorusbattle/' + str(cb.id))})


    return render_template("chorusbattles.html", info=info, icon=getUserIcon((session['username'] if 'username' in session else None)))

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
            return render_template('createchorusbattle.html', form=form, icon=getUserIcon((session['username'] if 'username' in session else None)))    
        creator_id = User.query.filter_by(username=session['username']).first().id
        newcb = ChorusBattle(form.name.data, form.description.data,
                             form.rules.data, form.prizes.data, form.video_link.data, 
                             form.start_date.data, form.no_of_rounds.data, creator_id)

        db.session.add(newcb)
        db.session.commit()

        return redirect(url_for('chorusInfo', cb=newcb.id))

    elif request.method == 'GET':
        return render_template('createchorusbattle.html', form=form, icon=getUserIcon((session['username'] if 'username' in session else None)))

@app.route('/chorusbattle/<cb>/judge/<entry>', methods=['GET', 'POST'])
def judgeEntry(cb=None, entry=None):
    """
    The route '/chorusbattle/<cb>/judge/<entry>' directs the judge to a form
    where he/she can grade an entry using a rubric.
    """
    if request.method == 'GET':
        return render_template("judgingtool.html", chorusBattle=cb, entry=entry, icon=getUserIcon((session['username'] if 'username' in session else None)))

@app.route('/chorusbattle/<cb>/entries/createround/', methods=['GET', 'POST'])
def createRound(cb=None):
    """
    The route '/create/round' will direct the user, who has to be a Judge,
    to the form where he/she will fill out information in order to add a round
    to the chorus battle he/she is hosting.
    After submitting the form, the user will be notified of any errors, if
    there are any. Otherwise, the round will be created.
    """
    form = CreateRoundForm()

    if request.method == 'POST':
        print(dir(form.deadline.widget))
        print((form.deadline.raw_data))
        if not form.validate():
            return render_template('createround.html', cb=cb, form=form, icon=getUserIcon((session['username'] if 'username' in session else None)))

        newRound = Round(cb, form.theme.data, form.deadline.data)
        db.session.add(newRound)
        # ChorusBattle.query.filter_by(id=cb).first().no_of_rounds += 1
        db.session.commit()

        # somehow redirect the user back to the chorus battle info page for
        # this particular chorus battle
        return redirect(url_for('chorusEntries', cb=cb))

    elif request.method == 'GET':
        return render_template('createround.html', cb=cb, form=form, icon=getUserIcon((session['username'] if 'username' in session else None)))


# work in progress
@app.route('/user/<username>/', methods=['GET'])
def getUserProfile(username=None):
    """
    The route '/user/<username>' directs the user to the profile page of
    the user with the specified username.
    """
    row = User.query.filter_by(username=username).first()
    if row:
        return render_template("userprofile.html", username=row.get_username(), role=row.get_role(), user_icon=getUserIcon(username), icon=getUserIcon((session['username'] if 'username' in session else None)))

    # return render_template("userprofile.html")

@app.route('/help/faq/', methods=['GET'])
def faq():
    """
    The route '/help/faq/' directs the user to the Frequently Asked Questions
    page. This page contains the user documentation which will assist the
    end users who are using the app.
    """
    return render_template("faq.html", icon=getUserIcon((session['username'] if 'username' in session else None)))

def getUserIcon(username):
    """ 
    This function grabs the user_icon from db based on queried username.
    """
    if not username:
        return username
    user_icon = User.query.filter_by(username=username).first().user_icon
    if user_icon:
        user_icon = b64encode(user_icon).decode('utf-8')
    return user_icon    