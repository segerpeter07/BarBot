# /barbot/__init__.py

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .views.profile import profile
from .views.home import home
from .views.settings import settings
from .views.admin import admin

from .models import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(profile, url_prefix='/<user_url_slug>')
app.register_blueprint(home)
app.register_blueprint(settings, url_prefix='/<user_url_slug>')
app.register_blueprint(admin, url_prefix='/<user_url_slug>')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bcyrpt = Bcrypt(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()
