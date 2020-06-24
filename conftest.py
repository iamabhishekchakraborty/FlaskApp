from __future__ import print_function
from pytest import fixture
from flask import Flask
from app import app


@fixture(scope='module')
def client():
    """Get a test client for your Flask app"""
    print("\n(Doing global fixture setup stuff!)")
    flask_app = Flask(__name__)
    tester = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield tester
    ctx.pop()


