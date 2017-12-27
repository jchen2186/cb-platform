"""
routes.py
This module contains the routes that allows flask to help navigate the
user to the templates.
"""


import os
import urllib.parse
import copy
import datetime
from base64 import b64encode
from sqlalchemy.sql.expression import func
from flask import flash, render_template, request, session, redirect, url_for
from cbapp import app
from .forms import SignupForm, LoginForm, CreateChorusBattleForm, CreateEntryForm,\
CreateRoundForm, CreateTeamForm, JudgeEntryForm, InviteTeamForm, NotificationForm
from .models import db, User, ChorusBattle, UserRole, Entry, Round, Team, user_teams,\
Notification, subscriptions, JudgeScore, judges

# pylint: disable=C0103
# pylint: disable=no-member

# connect app to the postgresql database (local to our machines)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgresql://postgres:1@localhost:5432/cbapp')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/cbapp')

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
        session['role'] = newuser.get_role()
        session['first_name'] = newuser.firstname
        return redirect(url_for('home'))
        # return render_template('home.html', propic=b64encode(propic).decode('utf-8'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/logout/')
def logout():
    """
    The route '/logout' will remove the user from the current session.
    """
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home/')
def home():
    """
    The route '/home' will redirect the user to the dashboard if the
    user is logged in. Otherwise, it will redirect the user to the login
    form in order to log in.
    """
    print(session.items())
    if 'username' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    # check team invites
    team_invitesQuery = db.session.query(user_teams).filter_by(user_id=user.id,
                                                               member_status='pending').all()
    team_invites = []
    for team in team_invitesQuery:
        team_invites.append(Team.query.filter_by(id=team.team_id).first())
    # check team requests
    owned_teams = Team.query.filter_by(leader_id=user.id).all()
    team_requests = []
    for owned_team in owned_teams:
        team_requestsQuery = db.session.query(user_teams).filter_by(team_id=owned_team.id,
                                                                    member_status='request').all()
        for team_request in team_requestsQuery:
            team_requests.append({
                'id': owned_team.id,
                'team_name': owned_team.team_name,
                'userID': team_request.user_id,
                'username': User.query.filter_by(id=team_request.user_id).first().username
                })
    # print(team_requests)
    # get 10 most recent notifications
    notif = Notification.get_notifications(user.id).paginate(1, 5, False).items
    subs = db.session.query(subscriptions).filter_by(user_id=User.get_id_by_username(session['username'])).all()
    sub_cbs = []

    # get the teams the user is associated with

    team_cbs=db.session.query(user_teams).filter_by(user_id=User.get_id_by_username(session['username'])).all()
    judge_cbs = db.session.query(User).join(judges).join(ChorusBattle).filter_by(id=User.get_id_by_username(session['username'])).all()
    my_cbs_id = []
    my_cbs = []
    print("team_cbs", team_cbs)
    for judge in judge_cbs:
        print("judge is", judge)
        if judge[0] not in my_cbs_id:
            my_cbs_id.append(judge[0])

    for team in team_cbs:
        # get the teams the user is in
        current_team = Team.query.filter_by(id=team[1]).first()
        print(current_team)
        # get the associated cb with the team
        if current_team.chorusbattle not in my_cbs_id:
            my_cbs_id.append(current_team.chorusbattle)

    print(my_cbs_id)
    for sub in subs:
        cb = ChorusBattle.query.filter_by(id=sub.chorusbattle_id).first()
        if cb:
            temp = {}
            temp['name'] = cb.name
            temp['id'] = cb.id
            sub_cbs.append(temp)
        
        

        
    for cbid in my_cbs_id:
        cb = ChorusBattle.query.filter_by(id=cbid).first()
        if cb:
            temp = {}
            temp['name'] = cb.name
            temp['id'] = cb.id
            my_cbs.append(temp)
        
        

       

    recs = ChorusBattle.query.order_by(func.random()).limit(3).all()
    print(recs)
    return render_template('home.html', recs=recs, notifications=notif,
                           subs=sub_cbs, my_cbs=my_cbs, team_requests=team_requests,
                           team_invites=team_invites,
                           icon=getUserIcon((session['username']\
                            if 'username' in session else None)))

@app.route('/home/notifications/')
@app.route('/home/notifications/<int:page>')
def viewNotifications(page=1):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first().id
    notifs = Notification.get_notifications(user).paginate(page, 10, False)
    notifications = notifs.items
    return render_template('viewNotifications.html', notifications=notifications,
                           notifs=notifs,
                           icon=getUserIcon((session['username']\
                            if 'username' in session else None)))

@app.route('/chorusbattle/<cb>/', methods=['GET'])
def chorusInfo(cb=None):
    """
    The route '/chorusbattle/<cb> will direct the user to a page where the user
    can find more information about the selected chorus battle, stored
    as the variable cb.
    """
    row = ChorusBattle.query.filter_by(id=cb).first()
    if row == None:
        return redirect(url_for('chorusBattleAll'))

    teams_query = Team.query.filter_by(chorusbattle=cb).all()
    judges_query = db.session.query(judges).filter_by(chorusbattle_id=cb).all()
    teams = []
    judges_list = []

    round_deadlines = []
    maxRound = row.no_of_rounds
    roundCount = len(Round.query.filter_by(chorusbattle=cb).all())
    print('roundCount', roundCount)
    for rd in range(1, roundCount+1):
        roundQuery = Round.query.filter_by(chorusbattle=cb, round_number=rd).first()
        deadline = roundQuery.deadline
        round_deadlines.append(deadline)

    for team in teams_query:
        temp = {}
        temp["id"] = team.id
        temp["team_name"] = team.team_name
        if team.team_logo:
            temp["team_logo"] = b64encode(team.team_logo).decode('utf-8')

        teams.append(temp)

    for judge in judges_query:
        temp = {}
        temp["user_id"] = judge.user_id
        temp['name'] = User.query.filter_by(id=judge.user_id).first().username

        judges_list.append(temp)

    cb_judges = []
    if len(judges_query) > 0:
        for judge in judges_query:
                user = User.query.filter_by(id=judge.user_id).first()

    if row:
        subbed = False
        if 'username' in session:
            current_user = User.query.filter_by(username=session['username']).first()
            user_id = current_user.id
            subbed = Notification.is_subscribed(user_id, cb)

        return render_template('chorusinfo.html', cb=row,
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)),
                               deadlines=round_deadlines,
                               maxRound=maxRound,
                               teams=teams,
                               subbed=subbed,
                               judges=judges_list)

@app.route('/chorusbattle/<cb>/subscribe')
def subscribe(cb=None):
    if 'username' not in session:
        return redirect(url_for('login'))

    current_user = User.query.filter_by(username=session['username']).first()
    user_id = current_user.id

    if not Notification.is_subscribed(user_id, cb):
        this_cb = ChorusBattle.query.filter_by(id=cb).first()
        current_user.subscriptions.append(this_cb)
        db.session.commit()
        chorusbattle_name = this_cb.name
        flash('You subscribed to '+ chorusbattle_name +"!")
        return redirect(url_for('chorusInfo', cb=cb, subbed=True))
    else:
        this_cb = ChorusBattle.query.filter_by(id=cb).first()
        chorusbattle_name = this_cb.name
        current_user.subscriptions.remove(this_cb)
        db.session.commit()
        flash('You are no longer subscribed to '+ chorusbattle_name +".")
        return redirect(url_for('chorusInfo', cb=cb, subbed=True))

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
        print(deadline, type(deadline))

        entries = Entry.query.filter_by(chorusbattle=cb, round_number=rd).all()
        for entry in entries:
            currRound.append({'id': entry.id, 'title':entry.title,
                              'owners':Team.query.filter_by(id=entry.team_id).first().team_name,
                              'description':entry.description, 'video_link':entry.video_link})
        rounds.append(currRound)

    subbed = False
    if 'username' in session:
        user_id = User.get_id_by_username(session['username'])
        subbed = Notification.is_subscribed(user_id, cb)

    return render_template('entries.html', entrysubbed=subbed, cb=row,
                           maxRound=maxRound, roundCount=roundCount, rounds=rounds,
                           icon=getUserIcon((session['username']\
                            if 'username' in session else None)))

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
            return render_template('createentry.html', cb=cb, rd=rd, form=form,
                                   icon=getUserIcon((session['username']\
                                    if 'username' in session else None)))
        newEntry = Entry(form.team_name.data, form.title.data, form.description.data,
                         form.video_link.data, cb, rd)

        db.session.add(newEntry)
        db.session.commit()

        return redirect(url_for('chorusEntries', cb=newEntry.chorusbattle))

    elif request.method == 'GET':
        return render_template('createentry.html', cb=cb, rd=rd, form=form,
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)))

@app.route('/team/<teamID>/', methods=['GET', 'POST'])
def team(teamID=None):
    """
    The route '/team/<name>' will direct the user to a page containing
    information about the selected chorus battle team, stored as the
    variable name.
    """

    team = Team.query.filter_by(id=teamID).first()
    # edit open_roles
    if request.method == 'POST':
        if 'open_roles' in request.form:
            team.open_roles = request.form['open_roles']
            flash('You have successfully changed the open roles.')
        if 'about' in request.form:
            team.about = request.form['about']
            flash('You have successfully changed the about section')
        db.session.commit()
    form = InviteTeamForm()
    team_users = db.session.query(user_teams).filter_by(team_id=teamID,
                                                        member_status='member').all()
    team_members = []
    for member in team_users:
        userObject = {
            'user': copy.deepcopy(User.query.filter_by(id=member.user_id).first())
        }
        userObject['role'] = UserRole.query.filter_by(id=userObject['user'].role_id).first().role_title.capitalize()

        user_icon = userObject['user'].user_icon
        if user_icon:
            userObject['user_icon'] = b64encode(user_icon).decode('utf-8')
        else:
            userObject['user_icon'] = None

        team_members.append(userObject)
    if team:
        team_logo = None
        if team.team_logo:
            team_logo = b64encode(team.team_logo).decode('utf-8')
        chorusBattle = None
        chorusBattle = ChorusBattle.query.filter_by(id=team.chorusbattle).first().name
        currentUser = User.query.filter_by(username=(session['username']\
                                            if 'username' in session else None)).first()
        if currentUser:
            team_user = db.session.query(user_teams).filter_by(user_id=currentUser.id,
                                                               team_id=teamID).first()
            print(team_user)
            if team_user:
                print(team_user.member_status)
            currentUser = currentUser.id
            return render_template('team.html', currentUser=currentUser,
                                   team_user=team_user, form=form,
                                   chorusBattle=chorusBattle, team=team,
                                   team_logo=team_logo, team_members=team_members,
                                   icon=getUserIcon((session['username']\
                                    if 'username' in session else None)))
        return render_template('team.html', currentUser=currentUser, team_user=None,
                               form=form, chorusBattle=chorusBattle, team=team,
                               team_logo=team_logo, team_members=team_members,
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)))
    return redirect(request.referrer or url_for('home'))

@app.route('/chorusbattle/<cb>/createteam/', methods=['GET', 'POST'])
def createTeam(cb=None):
    """
    The route '/create/team/' will direct the user to a form that
     will allow them to create a team
    """
    deadline = ChorusBattle.query.filter_by(id=cb).first().start_date
    if deadline:
        if datetime.datetime.now() > deadline:
            print(datetime.datetime.now(), '>', deadline)
            print(type(datetime.datetime.now()), '>', type(deadline))
            flash('Sorry, the deadline for joining this chorus battle has passed.')
            return redirect(request.referrer or url_for('chorusInfo', cb=cb))
    chorusrow = ChorusBattle.query.filter_by(id=cb).first()
    leader = User.query.filter_by(username=session['username']).first()
    # check if leader already created another team
    if chorusrow.teams:
        for team in chorusrow.teams:
            if team.leader_id == leader.id:
                flash('You already lead a team in this chorus battle.')
                return redirect(url_for('chorusInfo', cb=cb))

    form = CreateTeamForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('createteam.html', form=form, cb=cb,
                                   icon=getUserIcon((session['username']\
                                    if 'username' in session else None)))

        # check if team name exists in competition
        teams = Team.query.filter_by(team_name=form.team_name.data).all()
        for team in teams:
            print('team', team.team_name, 'in', str(team.chorusbattle))
            print('new', form.team_name.data, 'in', cb)
            if str(team.chorusbattle) == cb:
                flash('Team name is already registered in this chorus battle')
                return render_template('createteam.html',
                                       form=form, cb=cb,
                                       icon=getUserIcon((session['username']\
                                        if 'username' in session else None)))
        teampic = None
        if form.teampic.data:
            teampic = request.files.getlist('teampic')[0].read()

        print(form.members, '\n', form.members.entries, '\n', form.members.data)
        # create team
        newteam = Team(form.team_name.data, leader.id, teampic, cb)
        db.session.add(newteam)
        db.session.commit()
        # invite leader
        newteam.member.append(leader)
        db.session.commit()
        db.engine.execute("UPDATE user_teams " + \
            "SET member_status = 'member'" + \
            "WHERE user_id=" + str(leader.id) + " and team_id=" + str(newteam.id) + ";")
        flash('You have successfully created a team.')
        # invite members
        for member in form.members.data:
            invitee = User.query.filter_by(username=member).first()
            if invitee:
                checkTeams = []
                teamQuery = db.session.query(user_teams).filter_by(user_id=invitee.id,
                                                                   member_status='member').all()
                for t in teamQuery:
                    checkTeams.append(t.team_id)
                in_team = False
                for team in chorusrow.teams:
                    if team.id in checkTeams:
                        in_team = True
                        flash(invitee.username + ' already belongs to a team in this chorus battle.')
                if not in_team:
                    newteam.member.append(invitee)
                    flash('You have invited ' + invitee.username + '.')
            else:
                flash(member + ' is not a registered user.')
        db.session.commit()
        return redirect(url_for('team', teamID=newteam.id))
    return render_template('createteam.html', form=form, cb=cb,
                           icon=getUserIcon((session['username']\
                            if 'username' in session else None)))
@app.route('/team/<teamID>/invite/', methods=['GET', 'POST'])
def inviteTeam(teamID=None):
    """
    The route /team/<teamID>/invite/ allows a team leader to invite a user to their team
    """
    form = InviteTeamForm()
    print(dir(user_teams))
    if request.method == 'POST':
        team = Team.query.filter_by(id=teamID).first()
        if User.query.filter_by(username=session['username']).first().id == team.leader_id:
            invitee = User.query.filter_by(username=form.username.data).first()
            if invitee:
                team_user = db.session.query(user_teams).filter_by(user_id=invitee.id,
                                                                   team_id=teamID).first()
                if team_user:
                    flash('You have already invited ' + invitee.username + '.')
                else:
                    chorusrow = ChorusBattle.query.filter_by(id=team.chorusbattle).first()
                    checkTeams = []
                    teamQuery = db.session.query(user_teams).filter_by(user_id=invitee.id,
                                                                       member_status='member').all()
                    for t in teamQuery:
                        checkTeams.append(t.team_id)
                    in_team = False
                    for team in chorusrow.teams:
                        if team in checkTeams:
                            in_team = True
                            flash(invitee.username + ' already belongs to a team in this chorus battle.')
                    if not in_team:
                        team.member.append(invitee)
                        flash('You have invited ' + invitee.username + '.')
            else:
                flash(form.username.data + ' is not a registered user.')
        else:
            flash('You are not the team leader.')
        db.session.commit()
    return redirect(request.referrer or url_for('team', teamID=teamID))

@app.route('/team/<teamID>/request/', methods=['GET'])
def requestTeam(teamID=None):
    """
    The route /team/<teamID>/request/ allows users to request to join a team.
    """
    user = User.query.filter_by(username=session['username']).first()
    team_user = db.session.query(user_teams).filter_by(user_id=user.id, team_id=teamID).first()
    team_name = Team.query.filter_by(id=teamID).first().team_name
    if team_user:
        flash('You cannot request to join this team if you are already a member or if you declined an invitation.')
        return redirect(request.referrer or url_for('team', teamID=teamID))
    team = Team.query.filter_by(id=teamID).first()
    if team:
        team.member.append(user)
        db.session.commit()
        db.engine.execute("UPDATE user_teams " + \
            "SET member_status = 'request'" + \
            "WHERE user_id=" + str(user.id) + " and team_id=" + str(teamID) + ";")
        flash('You have requested to join ' + team_name + '.')
    else:
        return redirect(request.referrer or url_for('home'))
    return redirect(url_for('team', teamID=teamID))

@app.route('/team/<teamID>/accept/<userID>', methods=['GET'])
def acceptTeam(teamID=None, userID=None):
    """
    The route /team/<teamID>/accept/ allows team leaders to accept requested users.
    """
    user = User.query.filter_by(id=userID).first()
    if user:
        team_user = db.session.query(user_teams).filter_by(user_id=userID, team_id=teamID,
                                                           member_status='request').first()
        if team_user:
            db.engine.execute("UPDATE user_teams " + \
                "SET member_status = 'pending'" + \
                "WHERE user_id=" + str(user.id) + " and team_id=" + str(teamID) + ";")
            flash('You have invited ' + user.username + '.')
        else:
            flash('You cannot invite a user that is not requesting to join.')
    else:
        flash('You cannot invite a user that does not exist.')
    return redirect(request.referrer or url_for('home'))

@app.route('/team/<teamID>/reject/<userID>/', methods=['GET'])
def rejectTeam(teamID=None, userID=None):
    """
    The route /team/<teamID>/reject/ allows team leaders to reject users that
    requested to join.
    """
    user = User.query.filter_by(id=userID).first()
    if user:
        team_user = db.session.query(user_teams).filter_by(user_id=userID, team_id=teamID,
                                                           member_status='request').first()
        if team_user:
            db.engine.execute("UPDATE user_teams " + \
                "SET member_status = 'rejected'" + \
                "WHERE user_id=" + str(user.id) + " and team_id=" + str(teamID) + ";")
            flash('You have rejected ' + user.username + '.')
        else:
            flash('You cannot reject a user that is not requesting to join.')
    else:
        flash('You cannot reject a user that does not exist.')
    return redirect(request.referrer or url_for('home'))

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
            "WHERE user_id=" + str(userID) + " and team_id=" + str(teamID) + ";")
        flash('You have successfully joined ' + team_name + '.')
    else:
        flash('You are not invited to ' + team_name + '.')
    return redirect(request.referrer or url_for('home'))

@app.route('/team/<teamID>/decline/', methods=['GET'])
def declineTeam(teamID=None):
    """
    The route /team/<teamID>/decline/ allows users to decline a team invitation.
    """
    userID = User.query.filter_by(username=session['username']).first().id
    team_user = db.session.query(user_teams).filter_by(user_id=userID, team_id=teamID).first()
    team_name = Team.query.filter_by(id=teamID).first().team_name
    if team_user:
        if team_user.member_status == 'member':
            flash('You are a member of ' + team_name + ' already. Please contact your team leader to leave the team.')
            return redirect(request.referrer or url_for('home'))
        elif team_user.member_status == 'declined':
            flash('You already declined the invitation to join this team.')
            return redirect(request.referrer or url_for('home'))
        db.engine.execute("UPDATE user_teams " + \
            "SET member_status = 'declined'" + \
            "WHERE user_id=" + str(userID) + " and team_id=" + str(teamID) + ";")
        flash('You have declined to join ' + team_name + '.')
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


    return render_template("chorusbattles.html", info=info,
                           icon=getUserIcon((session['username']\
                            if 'username' in session else None)))

@app.route('/create/chorusbattle/', methods=['GET', 'POST'])
def createChorusBattle():
    """
    The route '/create/chorusbattle' will direct the user, who has
    to be a judge, to the form where he/she will fill out information
    relating to the chorus battle.
    After submitting the form, the user will be notified of any errors,
    if there are any. Otherwise, the chorus battle will be created.
    """
    form = CreateChorusBattleForm()

    # If the user is not a judge, redirect them to the home page.
    if session['role'] != 'Judge':
        return redirect(url_for('home'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('createchorusbattle.html', form=form,
                                   icon=getUserIcon((session['username']\
                                    if 'username' in session else None)))
        creator_id = User.query.filter_by(username=session['username']).first().id
        # Create a new chorus battle
        new_cb = ChorusBattle(form.name.data, form.description.data,
                              form.rules.data, form.prizes.data, form.video_link.data,
                              form.start_date.data, form.no_of_rounds.data, creator_id)

        # Add judges to chorus battle
        for judge in form.judges:
            team_judge = User.query.filter_by(username=judge.data).first()
            new_cb.judges.append(team_judge)

        db.session.add(new_cb)
        db.session.commit()

        return redirect(url_for('chorusInfo', cb=new_cb.id))

    elif request.method == 'GET':
        return render_template('createchorusbattle.html', form=form,
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)))

@app.route('/chorusbattle/<cb>/judge/notify', methods=['GET', 'POST'])
def writeNotification(cb=None):
    if 'username' not in session:
        return redirect(url_for('login'))

    # check if judge is a valid judge for this cb
    judges_query = db.session.query(judges).filter_by(chorusbattle_id=cb).all()
    current_user_id = User.get_user_id(session['username'])
    judges_list = []
    for judge in judges_query:
        judges_list.append(judge.user_id)
    if current_user_id not in judges_list:
        return redirect(url_for('chorusInfo',cb=cb))

    form = NotificationForm()

    if request.method == "GET":
        return render_template('notify.html', cb=cb,
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)), form=form)
    elif request.method == "POST":
        message = form.message.data
        user_id = User.get_id_by_username(session['username'])

        newNotif = Notification(user_id, cb, message)

        db.session.add(newNotif)
        db.session.commit()

        flash("Your notification has been posted!")
        return redirect(url_for('chorusInfo', cb=cb))

@app.route('/chorusbattle/<cb>/entries/<entry>/judge', methods=['GET', 'POST'])
def judgeEntry(cb=None, entry=None):
    """
    The route '/chorusbattle/<cb>/judge/<entry>' directs the judge to a form
    where he/she can grade an entry using a rubric.
    """
    # If user is not a judge, redirect the user to the chorus battle page
    if 'username' not in session:
        return redirect(url_for('home'))
    if session['role'] != 'Judge':
        return redirect(url_for('chorusInfo', cb=cb))

    # check if judge is a valid judge for this cb
    judges_query = db.session.query(judges).filter_by(chorusbattle_id=cb).all()
    current_user_id = User.get_user_id(session['username'])
    judges_list = []
    for judge in judges_query:
        judges_list.append(judge.user_id)
    if current_user_id not in judges_list:
        return redirect(url_for('chorusInfo',cb=cb))

    judge_id = User.get_user_id(session['username'])
    form = JudgeEntryForm()
    chorusbattle_info = ChorusBattle.query.filter_by(id=cb).first()
    entry_info = Entry.query.filter_by(id=entry).first()
    has_judged_before = JudgeScore.has_judged_before(judge_id, int(entry))
    if request.method == 'GET':
        if has_judged_before:
            judged_entry = JudgeScore.query.filter_by(judge_id=judge_id,
                                                      entry_id=entry).first()
            return render_template("judgingtool.html", has_judged_before=True,
                                   judged_entry=judged_entry,
                                   chorusbattle=chorusbattle_info,
                                   entry=entry_info, form=form,
                                   icon=getUserIcon((session['username']\
                                    if 'username' in session else None)))
        return render_template("judgingtool.html", has_judged_before=False,
                               chorusbattle=chorusbattle_info,
                               entry=entry_info, form=form,
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)))
    elif request.method == 'POST':

        if form.validate():
            judge_id = User.get_user_id(session['username'])
            new_judge_score = JudgeScore(judge_id, entry,
                                         form.vocals.data, form.vocals_comment.data,
                                         form.instrumental.data,
                                         form.instrumental_comment.data,
                                         form.art.data, form.art_comment.data,
                                         form.editing.data, form.editing_comment.data,
                                         form.transitions.data,
                                         form.transitions_comment.data)
            db.session.add(new_judge_score)
            db.session.commit()

            return redirect(url_for('chorusEntries', cb=cb))
        return render_template("judgingtool.html", has_judged_before=False,
                               chorusbattle=chorusbattle_info,
                               entry=entry_info, form=form,
                               icon=getUserIcon((session['username']\
                                    if 'username' in session else None)))


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
            return render_template('createround.html', cb=cb, form=form,
                                   icon=getUserIcon((session['username']\
                                    if 'username' in session else None)))

        newRound = Round(cb, form.theme.data, form.deadline.data)
        db.session.add(newRound)
        # ChorusBattle.query.filter_by(id=cb).first().no_of_rounds += 1
        db.session.commit()

        # somehow redirect the user back to the chorus battle info page for
        # this particular chorus battle
        return redirect(url_for('chorusEntries', cb=cb))

    elif request.method == 'GET':
        return render_template('createround.html', cb=cb, form=form,
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)))

@app.route('/community/', methods=['GET'])
def viewCommunity():
    """
    The route '/community/' directs the user to the community page
    where teams and other users can be viewed.
    """
    users = User.query.order_by(func.random()).limit(20).all()
    user_icons = []
    for user in users:
        user_icon = user.user_icon
        if user_icon:
            user_icons.append(b64encode(user_icon).decode('utf-8'))
        else:
            user_icons.append(None)
    teams = Team.query.order_by(func.random()).limit(20).all()
    team_icons = []
    team_chorusbattles = []
    for team in teams:
        team_logo = team.team_logo
        if team_logo:
            team_icons.append(b64encode(team_logo).decode('utf-8'))
        else:
            team_icons.append(None)
        team_chorusbattles.append(ChorusBattle.query.filter_by(id=team.chorusbattle).first().name)
    print(users, teams)
    return render_template('community.html', users=users, user_icons=user_icons,
                           teams=teams, team_chorusbattles=team_chorusbattles,\
                           team_icons=team_icons,
                           icon=getUserIcon((session['username']\
                            if 'username' in session else None)))

@app.route('/user/<username>/', methods=['GET', 'POST'])
def getUserProfile(username=None):
    """
    The route '/user/<username>' directs the user to the profile page of
    the user with the specified username.
    """
    row = User.query.filter_by(username=username).first()
    if row:
        if request.method == 'POST':
            if session['username'] == username:
                if 'current_status' in request.form:
                    row.current_status = request.form['current_status']
                    flash('You have successfully changed your status')
                if 'description' in request.form:
                    row.description = request.form['description']
                    flash('You have successfully changed your description')
                db.session.commit()
            return redirect(url_for('getUserProfile', username=username))
        teamQuery = db.session.query(user_teams).filter_by(user_id=row.id,
                                                           member_status='member').all()
        teams = []
        for team in teamQuery:
            t = Team.query.filter_by(id=team.team_id).first()
            team_chorusbattle = ChorusBattle.query.filter_by(id=t.chorusbattle).first().name
            teams.append({
                'id': t.id,
                'team_name': t.team_name,
                'cid': t.chorusbattle,
                'chorusbattle': team_chorusbattle
                })

        return render_template("userprofile.html", user=row, teams=teams,
                               role=row.get_role(), user_icon=getUserIcon(username),
                               icon=getUserIcon((session['username']\
                                if 'username' in session else None)))
    return redirect(request.referrer or url_for('index'))
    # return render_template("userprofile.html")

@app.route('/chorusbattle/<cb>/round/<round_number>', methods=['GET', 'POST'])
def chorusRound(cb=None,round_number=None):
    """
    The route '/chorusbattle/<cb>/round/<round_number>' directs a judge to a page
    for a round where they can choose a winner
    """
    # If user is not a judge, redirect them out of the page
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'Judge':
        return redirect(url_for('chorusInfo', cb=cb))
    round_id = db.session.query(Round.id).filter_by(chorusbattle=cb).first()
    round_info = db.session.query(Round).filter_by(id=round_id).first() 
    form = ChooseRoundWinnerForm()
    if request.method == 'GET':
        return render_template('chorusRound.html',cb=cb, round_number=round_number, round=round_id, form=form)
    else:
        if form.validate():
            winning_team_id = db.session.query(Team.id).filter_by(team_name=form.winning_entry.data).first()
            if winning_team_id:
                Round.choose_winner(round_id,winning_team_id)
                db.session.commit()
                return redirect(url_for('chorusInfo', cb=cb))
            else:
                flash('Invalid team name.')
                return render_template('chorusRound.html',cb=cb, round_number=round_number, round=round_id, form=form)
        else:
            return render_template('chorusRound.html',cb=cb, round_number=round_number, round=round_id, form=form)





@app.route('/help/faq/', methods=['GET'])
def faq():
    """
    The route '/help/faq/' directs the user to the Frequently Asked Questions
    page. This page contains the user documentation which will assist the
    end users who are using the app.
    """
    return render_template("faq.html",
                           icon=getUserIcon((session['username']\
                            if 'username' in session else None)))

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

@app.route("/search/", methods=["GET", "POST"])
def search():
    """
    The route '/search/' directs the user to a list of users, chorus battles,
    and teams that fit the given query.
    """
    resultsUsers = []
    resultsCB = []
    resultsTeams = []
    if request.method == "POST":
        if request.form["search"] == "":
            return render_template("searchresult.html", resultsUsers=resultsUsers,
                                   resultsCB=resultsCB, resultsTeams=resultsTeams)
        else:
            for user in User.query.all():
                if request.form["search"].lower() in user.username.lower():
                    userInfo = []
                    userInfo.append(user.username)
                    userInfo.append(user.description)
                    resultsUsers.append(userInfo)
            for chorusbattle in ChorusBattle.query.all():
                if request.form["search"].lower() in chorusbattle.name.lower():
                    cbinfo = []
                    cbinfo.append(chorusbattle.id)
                    cbinfo.append(chorusbattle.name)
                    cbinfo.append(chorusbattle.description)
                    resultsCB.append(cbinfo)
            for team in Team.query.all():
                if request.form["search"].lower() in team.team_name.lower():
                    teamInfo = []
                    teamInfo.append(team.id)
                    teamInfo.append(team.team_name)
                    teamInfo.append(team.about)
                    resultsTeams.append(teamInfo)
        return render_template("searchresult.html", resultsUsers=resultsUsers,
                               resultsCB=resultsCB, resultsTeams=resultsTeams)
