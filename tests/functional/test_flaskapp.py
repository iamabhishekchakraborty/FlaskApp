import pytest
from flask import Flask
from app import *


def test_home_status_code_ok():
    test = app.test_client()
    resp = test.get('/')
    assert resp.status_code == 200
