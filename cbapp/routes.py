from flask import render_template, request
from forms import SignupForm, LoginForm
from models import db, User #, ChorusBattle, UserRole, Entry
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
    form = LoginForm()

    if request.method == 'POST':
        # temporary, change later
        return 'Success'
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        # temporary, change later
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, 
                form.password.data, form.username.data, form.role.data)
            db.session.add(newuser)
            db.session.commit()
            return 'Success'
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/chorusinfo/<cb>', methods=['GET'])
def chorusInfo(cb=None):
    return render_template('chorusinfo.html', chorusTitle=cb)
