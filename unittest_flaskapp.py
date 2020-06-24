import unittest
import xmlrunner
import tempfile
import re
from app import *


class FlaskApp(unittest.TestCase):
    def test_hello(self):
        tester = app.test_client(self)
        rv = tester.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertTrue(b'Welcome to Flask App' in rv.data)

    def test_hello_index(self):
        tester = app.test_client(self)
        rv = tester.get('/index')
        self.assertEqual(rv.status, '200 OK')
        self.assertTrue(b'I am here to help!' in rv.data)

    def test_all(self):
        tester = app.test_client(self)
        pages = ['/', 'index']
        for page in pages:
            rv = tester.get(page, content_type='html/text')
            self.assertEqual(rv.status, '200 OK')

    def test_hello_random(self):
        tester = app.test_client(self)
        rv = tester.get('/random', content_type='html/text')
        self.assertEqual(rv.status_code, 404)
        self.assertTrue(b'does not exist' in rv.data)


if __name__ == '__main__':
    ############# To Generate Test Reports  #############
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    #####################################################
    unittest.main()
