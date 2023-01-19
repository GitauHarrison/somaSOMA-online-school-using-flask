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

    def tearDown(self):
        db.drop_all() # < --- discard database after each test
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_elearning_app(self):
        assert self.app is not None
        assert app == self.app


# Redirection

# Access to templates

# Authentication
