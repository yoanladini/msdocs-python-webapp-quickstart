import os
import unittest
from flask import Flask
from app import app
from unittest.mock import patch
import io


class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Request for index page received', fake_stdout.getvalue())

    def test_favicon(self):
        response = self.app.get('/favicon.ico')
        self.assertEqual(response.status_code, 200)

    def test_hello_with_name(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            data = {'name': 'John Doe'}
            response = self.app.post('/hello', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Request for hello page received', fake_stdout.getvalue())
            self.assertIn(b'John Doe', response.data)

    def test_hello_without_name(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            response = self.app.post('/hello', data={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Request for hello page received with no name or blank name -- redirecting', fake_stdout.getvalue())
            self.assertEqual(response.request.path, '/')

if __name__ == '__main__':
    unittest.main()