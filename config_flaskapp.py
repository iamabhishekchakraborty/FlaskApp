import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password'
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en-US', 'en-GB', 'en-CA']
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    FLASK_RUN_PORT = 8000


class TestingConfig(Config):
    TESTING = True
