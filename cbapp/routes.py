from flask import render_template, request, session, redirect, url_for
from .forms import SignupForm, LoginForm
from .models import db, User, ChorusBattle, UserRole, Entry
from cbapp import app

# connect app to the postgresql database (local to our machines)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cbapp'
db.init_app(app)
app.secret_key = 'development-key'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html', form=form)
        else:
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user is not None and user.check_password(password):
                session['username'] = form.username.data
                return redirect(url_for('home'))
            else:
                # no error is displayed when user logs in with wrong credentials yet
                # this needs to be added
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
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
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/chorusinfo/<cb>', methods=['GET'])
def chorusInfo(cb=None):
    return render_template('chorusinfo.html', chorusTitle=cb)


@app.route('/entries/<int:id>',methods=['GET'])
def entries(id):
    chorusBattle = ChorusBattle.query.get_or_404(id)
    return render_template('entries.html', chorusTitle=cb)

@app.route('/team/<name>', methods=['GET'])
def team(name=None):
    return render_template('team.html')

