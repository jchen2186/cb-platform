from flask import Flask
app = Flask(__name__)       # pylint: disable=invalid-name
import cbapp.routes    # pylint: disable=wrong-import-position