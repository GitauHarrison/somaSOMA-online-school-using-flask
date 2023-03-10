from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, \
    SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, \
    Regexp, ValidationError
import phonenumbers
from app.models import User


# ========================================
# USER LOGIN
# ========================================


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'autofocus': True, 'placeholder': 'muthonigitau'})
    password = PasswordField(
        'Password:',
        validators=[DataRequired(), Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               message='Password must be at least 8 characters long and '
               'contain at least one letter and one number.')],
        render_kw={'placeholder': 'Example: somaSOMA123'})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


# ========================================
# END OF USER LOGIN
# ========================================



# ========================================
# PASSWORD RESET
# ========================================



class RequestPasswordResetForm(FlaskForm):
    """User can request for a password reset"""
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'autofocus': True, 'placeholder': 'You have access to this email address'})
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """User can change their password"""
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               message='Password must be at least 8 characters long and '
               'contain at least one letter and one number.')],
        render_kw={'autofocus':True, 'placeholder': 'Password'})
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


# ========================================
# END OF PASSWORD RESET
# ========================================



# ========================================
# USER REGISTRATION

# Define a base form
# Let children inherit the parent form
# ========================================


class UserForm(FlaskForm):
    """General User Data"""
    first_name = StringField(
        'First Name',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'autofocus': True, 'placeholder': 'Muthoni'})
    last_name = StringField(
        'Last Name',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'Gitau'})
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'muthonigitau'})
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'muthonigitau@email.com'})
    phone_number = StringField(
        'Phone Number',
        validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField(
        'Password:',
        validators=[DataRequired(), Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               message='Password must be at least 8 characters long and '
               'contain at least one letter and one number.')],
        render_kw={'placeholder': 'Example: somaSOMA123'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'Confirm Your Password Above'})

    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self, phone):
        p = phonenumbers.parse(phone.data)
        try:
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError) as exc:
            raise ValidationError('Invalid phone number.\n\n', exc ) from exc


class ParentRegistrationForm(UserForm):
    """Parent Registration Form"""
    current_residence = StringField(
        'Current Residence',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'Roselyn, Nairobi'})
    submit = SubmitField('Register')



class StudentRegistrationForm(UserForm):
    """Student Registration Form"""
    age = SelectField(
        'Age',
        choices=[            
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17')
            ],
        validators=[DataRequired()],
        render_kw={'placeholder': 'Between 6 - 17 years'})
    school = StringField(
        'School',
        validators=[DataRequired(), Length(min=2, max=64)],
        render_kw={'placeholder': 'Student\'s formal school'})
    coding_experience = SelectField(
        'Coding Experience',
        choices=[
            ('No experience', 'No experience'),
            ('Basic experience', 'Basic experience'),
            ('A lot of experience', 'A lot of experience'),
        ],
        validators=[DataRequired(), Length(min=2, max=64)])
    program = SelectField(
        'What Are You Interested In?',
        choices=[
            ('Tailwind CSS', 'Tailwind CSS'),
            ('Python', 'Python'),
            ('Javascript', 'JavaScript'),
        ],
        validators=[DataRequired(), Length(min=2, max=64)])
    program_schedule = SelectField(
        'Choose A Learning Schedule',
        choices=[
            ('Once A Week', 'Once A Week'),
            ('Three Times A Week', 'Three Times A Week'),
            ('All Week Days', 'All Week Days'),
        ],
        validators=[DataRequired(), Length(min=2, max=64)])
    cohort = SelectField(
        'Learning Group',
        choices=[
            ('Learning Group 1', 'Learning Group 1'),
            ('Learning Group 2', 'Learning Group 2'),
            ('Learning Group 3', 'Learning Group 3'),
        ],
        validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Register')



class AdminRegistrationForm(UserForm):
    """Admin Registration Form"""
    current_residence = StringField(
        'Current Residence',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'Roselyn, Nairobi'})
    department = SelectField(
        'Department',
        choices=[
        ('Finance', 'Finance'),
        ('Teaching', 'Teaching'),
        ('Content Creation', 'Content Creation'),
        ('Human Resources', 'Human Resources'),
        ],
        validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Register')



class TeacherRegistrationForm(UserForm):
    """Teacher Registration Form"""
    current_residence = StringField(
        'Current Residence',
        validators=[DataRequired(), Length(1, 64)],
        render_kw={'placeholder': 'Roselyn, Nairobi'})
    course = SelectField(
        'Teaching Course',
        choices=[
            ('Tailwind CSS', 'Tailwind CSS'),
            ('Python', 'Python'),
            ('Javascript', 'JavaScript'),
        ],
        validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField('Register')



# ========================================
# END OF USER REGISTRATION
# ========================================



# ========================================
# TWO FACTOR AUTHENTICATION
# ========================================

# Verify token sent

class VerifyForm(FlaskForm):
    """token verification form"""
    token = StringField(
        'Token',
        validators=[DataRequired()],
        render_kw={'autofocus': True, 'placeholder': 'Enter token sent'})
    submit = SubmitField('Verify')



# Disable 2fa

class DisableForm(FlaskForm):
    """User can disable 2FA"""
    submit = SubmitField('Disable')



# ========================================
# END OF TWO FACTOR AUTHENTICATION
# ========================================


# ========================================
# EMAIL
# ========================================


class EmailForm(FlaskForm):
    subject = StringField(
        'Subject',
        validators=[DataRequired()],
        render_kw={'autofocus':True, 'placeholder': 'Markdown enabled'})
    body = TextAreaField(
        'Body',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Markdown enabled'})
    closing = SelectField(
        'Closing',
        choices=[('Kind Regards', 'Kind Regards')],
        validators=[DataRequired()])
    signature = SelectField(
        'Signature',
        choices=[],
        validators=[DataRequired()])
    submit = SubmitField('Create Email')


# ========================================
# END OF EMAIL
# ========================================


# Unsubscribe from newsletter


class UnsubscribeForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'autofocus': True, 'placeholder': 'Your subscription email'})
    submit = SubmitField('Unsubscribe')

# =============
# Profile Edits
# =============

class EditUsernameForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class EditEmailForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(min=2, max=64)],
        render_kw={'placeholder': 'You have access to this email address'})
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')


class EditPhoneForm(FlaskForm):
    phone = StringField(
        'Phone Number',
        validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')

    def validate_phone(self, phone):
        p = phonenumbers.parse(phone.data)
        try:
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number.')

# Parent

class EditResidenceForm(FlaskForm):
    residence = StringField(
        'Residence',
        validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')


# Student

class EditSchoolForm(FlaskForm):
    school = StringField(
        'School',
        validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')

# =============
# End of Profile Edits
# =============


# =================================
# Lesson Quizes
# =================================

# ------
# Flask
# ------

class FlaskChapter2QuizForm(FlaskForm):
    question1 = SelectField(
        'Which of the following tags is used to create a link in HTML?',
        choices=[
            ('<a>', '<a>'),
            ('<body>', '<body>'),
            ('<p>', '<p>'),
            ('<em>', '<em>')
            ],
        validators=[DataRequired()])
    question2 = SelectField(
        'Where within an HTML structure do you link a CSS file?',
         choices=[
            ('<footer>', '<footer>'),
            ('<body>', '<body>'),
            ('<head>', '<head>'),
            ('<title>', '<title>')
            ],
        validators=[DataRequired()])
    question3 = SelectField(
     'Which option below is the correct way to style a <p>(paragraph) element?',
         choices=[
            ('p{color = orange;}', 'p{color = orange;}'),
            ('p{color = orange}', 'p{color = orange}'),
            ('p{color: orange;}', 'p{color: orange;}'),
            ('p{color == orange;}', 'p{color == orange;}')
            ],
        validators=[DataRequired()])
    question4 = SelectField(
        'How do you remove any decoration from a link (<a>) using CSS?',
            choices=[
                ('a{text-decoration: underline;}', 'a{text-decoration: underline;}'),
                ('a{text-decoration: none;}', 'a{text-decoration: none;}'),
                ('a{text-decoration: strikethrough;}', 'a{text-decoration: strikethrough;}'),
                ('a{text-decoration: all;}', 'a{text-decoration: all;}')
                ],
            validators=[DataRequired()])
    submit = SubmitField('Submit')


class FlaskChapter3QuizForm(FlaskForm):
    question1 = SelectField(
        'What is used to track changes in a repository?',
        choices=[
            ('Python', 'Python'),
            ('Tracker', 'Tracker'),
            ('Git', 'Git'),
            ('VS Code', 'VS Code')
            ],
        validators=[DataRequired()])
    question2 = SelectField(
        'What command is used to check if there has been changes to a git repository?',
         choices=[
            ('git status', 'git status'),
            ('Install github', 'Install github'),
            ('git branch -M main', 'git branch -M main'),
            ('git push origin -u main', 'git push origin -u main')
            ],
        validators=[DataRequired()])
    question3 = SelectField(
     'How do you add the changes in a file to version control?',
         choices=[
            ('git install <you-filename.ext>', 'git install <you-filename.ext>'),
            ('git add <you-filename.ext>', 'git add <you-filename.ext>'),
            ('git status <you-filename.ext>', 'git status <you-filename.ext>'),
            ('git init <you-filename.ext>', 'git init <you-filename.ext>')
            ],
        validators=[DataRequired()])
    question4 = SelectField(
        'How do you make a repository trackable by git?',
            choices=[
                ('flask run git', 'flask run git'),
                ('git init', 'git init'),
                ('git push origin main', 'git push origin main'),
                ('git status', 'git status')
                ],
            validators=[DataRequired()])
    question5 = SelectField(
        'How can a repository be downloaded from GitHub?',
            choices=[
                ('download <repo-name>', 'download <repo-name>'),
                ('pip3 download <repo-name>', 'pip3 download <repo-name>'),
                ('source venv/bin/download', 'source venv/bin/download'),
                ('git clone <link-to-repo>', 'git clone <link-to-repo>')
                ],
            validators=[DataRequired()])
    submit = SubmitField('Submit')



class FlaskChapter4QuizForm(FlaskForm):
    question1 = SelectField(
        'Which programming language has been used to create the flask framework?',
        choices=[
            ('HTML', 'HTML'),
            ('CSS', 'CSS'),
            ('Flask', 'Flask'),
            ('Python', 'Python')
            ],
        validators=[DataRequired()])
    question2 = SelectField(
        'Which command is used to create a virtual environment?',
         choices=[
            ('touch venv', 'touch venv'),
            ('python3 -m venv venv', 'python3 -m venv venv'),
            ('pip3 install flask', 'pip3 install flask'),
            ('flask run', 'flask run')
            ],
        validators=[DataRequired()])
    question3 = SelectField(
     'Which file is used to list select files to be ignored by git?',
         choices=[
            ('git', 'git'),
            ('main.py', 'main.py'),
            ('.gitignore', '.gitignore'),
            ('requirements.txt', 'requirements.txt')
            ],
        validators=[DataRequired()])
    question4 = SelectField(
        'How would you initialize a repository using git?',
            choices=[
                ('flask run git', 'flask run git'),
                ('git init', 'git init'),
                ('git push origin main', 'git push origin main'),
                ('git status', 'git status')
                ],
            validators=[DataRequired()])
    question5 = SelectField(
        'What is a README.md file used for?',
            choices=[
                ('To explain a project more', 'To explain a project more'),
                ('To read code', 'To read code'),
                ('To talk about your skills', 'To talk about your skills'),
                ('To push to GitHub', 'To push to GitHub')
                ],
            validators=[DataRequired()])
    submit = SubmitField('Submit')


# ------
# End of Flask
# ------

# =================================
# End of Profile Edits
# =================================
