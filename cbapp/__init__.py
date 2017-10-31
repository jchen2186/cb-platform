from flask import Flask
app = Flask(__name__)       # pylint: disable=invalid-name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cbplatform'
import cbapp.routes    # pylint: disable=wrong-import-position