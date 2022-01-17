from flask import Flask, Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_pyfile('config.py')

    return app
