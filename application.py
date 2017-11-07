from flask import Flask
from cbapp import app

if __name__ == '__main__':
    app.debug = True
    app.run()