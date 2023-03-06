from app import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from time import time
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# =================
# Application Users
# =================


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, default='First Name')
    last_name = db.Column(db.String(64), index=True, default='Last Name')
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(20), default='+254700111222')
    verification_phone = db.Column(db.String(20))
    active = db.Column(db.Boolean, nullable=False, default=True)
    delete_account = db.Column(db.Boolean, default=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    type = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'
    }

    def __repr__(self):
        return f'User: {self.username} {self.verification_phone}'

    def two_factor_enabled(self):
        return self.verification_phone is not None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        # override UserMixin property which always returns true
        # return the value of the active column instead
        return self.active

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'



class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    age = db.Column(db.Integer, default=6) 
    school = db.Column(db.String(64), default='Lean Sigma')
    coding_experience = db.Column(db.String(64), default='None')
    program = db.Column(db.String(64), default='Introduction to Flask')
    program_schedule = db.Column(db.String(64), default='Crash')
    cohort = db.Column(db.Integer, default=1)

    # Multiple join conditions where more than one foreign key is used
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id', ondelete='CASCADE'))
    parent = db.relationship(
        'Parent', backref='parent', foreign_keys=[parent_id], passive_deletes=True)


    __mapper_args__ = {
        'polymorphic_identity': 'student',
        'polymorphic_load': 'inline'
    }

    def __repr__(self):
        return f'Student: {self.first_name} | {self.program}'


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    course = db.Column(db.String(64), default='Flask')
    current_residence = db.Column(db.String(64), default='Roselyn, Nairobi')
    attendance = db.relationship(
        'StudentAttendance', backref='teacher', lazy='dynamic', passive_deletes=True)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
        'polymorphic_load': 'inline'
    }

    def __repr__(self):
        return f'Teacher: {self.first_name} | {self.course}'


class Parent(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    current_residence = db.Column(db.String(64), default='Roselyn, Nairobi')

    __mapper_args__ = {
        'polymorphic_identity': 'parent',
        'polymorphic_load': 'inline'
    }

    def __repr__(self):
        return f'Parent: {self.first_name} | {self.residence}'


class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    current_residence = db.Column(db.String(64), default='Roselyn, Nairobi')
    department = db.Column(db.String(64), default='Administration')

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'polymorphic_load': 'inline'
    }

    def __repr__(self):
        return f'Admin: {self.first_name} | {self.department}'

# =================
# End of Application Users
# =================

# =================
# Classroom Management
# =================


class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(64), index=True, default='Student', nullable=False)
    program = db.Column(db.String(64))
    cohort = db.Column(db.String(64))
    program_schedule = db.Column(db.String(64))
    lesson_number = db.Column(db.Integer, default=1)
    hours = db.Column(db.Integer, default=0)
    lesson_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'))

    def as_dict(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}


# =================
# End of classroom management
# =================


# =================
# Newsletter
# =================

class Newsletter_Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    num_newsletter = db.Column(db.Integer, nullable=False)
    email_confirmed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    subscription_status = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'Email: {self.email}'

    def is_active(self):
        # Override UserMixin property which always returns True
        # Return the value from the active column instead
        return self.subscription_status is True


# =================
# End of newsletter
# =================



# =================
# Emails sent out
# =================


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    closing = db.Column(db.String(50), nullable=False)
    bulk = db.Column(db.String(30), default='Bulk')
    signature = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    allow = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'Subject: {self.subject}'


# =================
# End of emails sent out
# =================
