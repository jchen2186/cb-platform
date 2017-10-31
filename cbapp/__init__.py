from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from models import db

app = Flask(__name__)       # pylint: disable=invalid-name

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cbplatform'
# db = SQLAlchemy(app)
# db.init_app(app)

import cbapp.routes    # pylint: disable=wrong-import-position

