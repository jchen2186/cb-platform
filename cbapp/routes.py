from flask import render_template
from flask import request
if __name__ != '__main__':
	from cbapp import app
else:
	from flask import Flask
	app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/chorusinfo/<cb>', methods=['GET'])
def chorusInfo(cb=None):
    return render_template('chorusinfo.html', chorusTitle=cb)

if __name__ == '__main__':
	app.run(debug=True)