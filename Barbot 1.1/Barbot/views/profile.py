# /barbot/views/profile.py

from flask import Blueprint, render_template, g
from flask_login import login_required, current_user

from ..models import User

profile = Blueprint('profile', __name__)


@profile.url_value_preprocessor
def get_profile_owner(endpoint, values):
    query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
    g.profile_owner = query.first_or_404()


@profile.route('/')
@login_required
def homescreeen():
    # do some stuff
    return render_template('profile/homescreeen.html')


@profile.route('/feed')
@login_required
def feed():
    # do some stuff
    return render_template('profile/feed.html')
