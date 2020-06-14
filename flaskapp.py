from flask import Flask, render_template, request, make_response
import config
from dotenv import load_dotenv
import os

# APP_SETTINGS = os.environ['APP_SETTINGS']
app = Flask(__name__)
app.config.from_object(config.Config)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(config.DevelopmentConfig)


@app.route('/')
def hello():
    return render_template('home.html', title='Home')


@app.route('/index')
def index():
    user = {'username': 'Abhishek'}
    posts = [
        {
            'author': {'username': 'CES'},
            'body': 'I am here to help!'
        }
    ]
    return render_template('index.html', title='Index', user=user, posts=posts)


@app.route('/<page_name>')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' % page_name, 404)
    return response


def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    app.run()
    # app.run(host='35.222.253.165',port=8000)
