from flask import render_template, flash, redirect, url_for, request
from flask_cors import CORS
from flaskapp import app
from os import environ, getcwd
import getpass

# getUser = lambda: environ["USERNAME"] if "C:" in getcwd() else environ["USER"]
# username = getUser()
username = getpass.getuser()


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Abhishek'}
    posts = [
        {
            'author': {'username': 'CES'},
            'body': 'I am here to help!'
        }
    ]
    return render_template('index.html', title='Home', user=username, posts=posts)

