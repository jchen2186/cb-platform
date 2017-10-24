from flask import render_template
from flask import request
from cbapp import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')