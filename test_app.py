"""
Testing all aspects of the application
"""

# Database configuration is imported first prior to
# all other configurations

import os
os.environ['DATABASE_URL'] = 'sqlite://'

from app import app, db
import unittest
from app.models import Parent, Student, User
from datetime import datetime, timedelta
from time import time
import jwt


class TestElearningApp(unittest.TestCase):

    def setUp(self):
        self.app = app

        # Disable csrf protection
        self.app.config['SECRET_KEY'] = 'testKEY'
        self.app.config['WTF_CSRF_ENABLED'] = False

        # Application context
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()                       # < --- create database during setup
        self.add_parent_to_db()               # < --- populate parent db
        self.client = self.app.test_client()  # < --- test client

    def tearDown(self):
        db.drop_all()                         # < --- discard database after each test
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

    # =====================
    # User
    # =====================

    def test_password_hashing(self):
        user = User(username='testuser')
        user.set_password('testuser2023')
        assert user.check_password('muthoni') == False
        assert user.check_password('testuser2023') == True

    def test_avatar(self):
        user = User(username='testuser', email='testuser@email.com')
        assert user.avatar(36) == ('https://www.gravatar.com/avatar/'
                                    '04678e8bacf37f21ebfbcdddefad9468'
                                    '?d=identicon&s=36')

    def test_reset_password_token(self):
        """Test generation of password reset token"""
        user = User(username='testuser', email='testuser@email.com')

        assert jwt.encode({'reset_password': user.email},'secret', algorithm='HS256') == \
            ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXNldF9wYXNzd29yZCI6InRlc'
             '3R1c2VyQGVtYWlsLmNvbSJ9.t__XarhVUwMSwekw_QsoipBREdvLjcl7kCwqwKlfnB8')

    def test_verify_password_reset_token(self, expires_in=600):
        """Verify the token generated"""
        user = User(username='testuser', email='testuser@email.com')

        token = jwt.encode(
                {'reset_password': user.email, 'exp': time() + expires_in},
                'secret',
                algorithm='HS256'
            )
        token = jwt.encode({'reset_password': 'testuser@email.com'},'secret',algorithm='HS256')
        email = jwt.decode(token, 'secret', algorithms=['HS256'])['reset_password']
        assert email == 'testuser@email.com'

    # =====================
    # End of user testing
    # =====================

    # =====================
    # Parent
    # =====================

    def add_parent_to_db(self):
        parent = Parent(
            first_name='Test',
            last_name='User',
            username='testuser',
            email='testuser@email.com',
            phone_number='+254700111222',
            residence='Roselyn, Nairobi'
        )
        parent.set_password('testuser2023')
        db.session.add(parent)
        db.session.commit()

    def parent_login(self):
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testuser2023'
        })    

    def test_parent_registration_form(self):
        response = self.client.get('/register')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # All these fields must be included
        assert 'name="first_name"' in html
        assert 'name="last_name"' in html
        assert 'name="username"' in html
        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'name="confirm_password"' in html
        assert 'name="phone_number"' in html
        assert 'name="residence"' in html
        assert 'name="register"' in html

    def test_mismatched_passwords_during_parent_registration(self):
        response = self.client.post('/register', data={
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'testuser2023',
            'confirm_password': 'testuser2023',
            'phone_number': '+254700111222',
            'residence': 'Roselyn, Nairobi'
        })
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Field must be equal to confirm_password' in html

    def test_parent_registration(self):
        response = self.client.post('/register/parent', data={
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'testuser2023',
            'confirm_password': 'testuser2023',
            'phone_number': '+254700111222',
            'residence': 'Nairobi'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/login'            # <--- redirected to the login page

    def test_parent_login(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testuser2023'
        }, follow_redirect=True)
        assert response.status_code == 200
        assert response.request.path == '/profile'
        html = response.get_data(as_text=True)
        assert 'Hi, testuser!' in html    

    def test_parent_register_child(self):
        self.parent_login()
        response = self.client.post('/register/child', data={
            'first_name': 'test',
            'last_name': 'student',
            'username': 'teststudent',
            'email': 'teststudent@email.com',
            'password': 'teststudent2023',
            'confirm_password': 'teststudent2023',
            'phone_number': '+254700111222',
            'school': 'Roselyn Academy',
            'age': 10,
            'coding_experience': 'None',
            'program': 'Introduction to Web Development',
            'cohort': 1,
            'program_schedule': 'Crash'
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Child successfully registered' in html
        assert response.request.path == '/profile'

    # =====================
    # End of parent testing
    # =====================

    # =====================
    # Student
    # =====================


    # =====================
    # End of student testing
    # =====================

    # =====================
    # Teacher
    # =====================


    # =====================
    # End of teacher testing
    # =====================

    # =====================
    # Admin
    # =====================


    # =====================
    # End of admin testing
    # =====================
