from flask import Flask, request
from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_babel import Babel
import logging
import os

app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)

# babel = Babel(app)


# @babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


from app import routes, errors
