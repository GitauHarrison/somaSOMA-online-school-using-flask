# Database configuration is imported first prior to
# all other configurations

import os
os.environ['DATABASE_URL'] = 'sqlite://'

from app import app, db
import unittest


class TestElearningApp(unittest.TestCase):

    # Application context

    def setUp(self):
        self.app = app
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all() # < --- create database during setup
        self.client = self.app.test_client() # < --- test client

    def tearDown(self):
        db.drop_all() # < --- discard database after each test
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_elearning_app(self):
        assert self.app is not None
        assert app == self.app

    def test_home_page_access(self):
        ''''''
        response = self.client.get('/')
        response_home = self.client.get('/home')
        assert response.status_code == 200
        assert response_home.status_code == 200


# Redirection

# Access to templates

# Authentication
