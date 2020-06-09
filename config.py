import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password'
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en-US', 'en-GB', 'en-CA']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
