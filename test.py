import unittest
import xmlrunner
import app
import re


class FlaskApp(unittest.TestCase):
    def setUp(self):
        FlaskApp.app.testing = True
        self.app = FlaskApp.app.test_client()

    def test_hello(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'I am here to help!\n')

    def test_hello_index(self):
        rv = self.app.get('/index/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'I am here to help!\n')


if __name__ == '__main__':
    ############# To Generate Test Reports  #############
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    #####################################################
    unittest.main()
