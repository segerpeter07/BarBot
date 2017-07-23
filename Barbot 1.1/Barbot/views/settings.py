# /barbot/views/settings.py

from flask import Blueprint, render_template, g
from flask_login import login_required, current_user

from ..models import User

settings = Blueprint('settings', __name__)


@settings.url_value_preprocessor
def get_settings_owner(endpoint, values):
    query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
    g.settings_owner = query.first_or_404()


@settings.route('/settings')
@login_required
def overview():
    # do some stuff
    return render_template('settings/overview.html')


@settings.route('/settings/change')
@login_required
def change_settings():
    # do some stuff
    return render_template('settings/change.html')
