from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
moment = Moment(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
boostrap = Bootstrap(app)

from app import routes, models, errors
