from flask import render_template
from flask import request
from cbapp import app
from forms import SignupForm, LoginForm

if __name__ != '__main__':
	from cbapp import app
else:
	from flask import Flask
	app = Flask(__name__)

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
        # temporary, change later
        return 'Success'
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/chorusinfo/<cb>', methods=['GET'])
def chorusInfo(cb=None):
    return render_template('chorusinfo.html', chorusTitle=cb)

if __name__ == '__main__':
	app.run(debug=True)