# /barbot/views/admin.py

from flask import Blueprint, render_template, g
from ..models import User
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)


@admin.url_value_preprocessor
def get_admin_owner(endpoint, values):
    query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
    g.admin_owner = query.first_or_404()


@admin.route('/admin')
@login_required
def overview():
    # do some stuff
    return render_template('admin/overview.html')


@admin.route('/admin/settings')
@login_required
def settings():
    # do some stuff
    return render_template('admin/settings.html')


@admin.route('/admin/feed')
@login_required
def feed():
    # do some stuff
    render_template('admin/feed.html')


@admin.route('admin/payment')
@login_required
def payment():
    # do some stuff
    render_template('admin/payment.html')


@admin.route('admin/new_party')
@login_required
def new_party():
    # do some stuff
    render_template('admin/new_party.html')


@admin.route('admin/logout')
@login_required
def logout():
    # do some stuff
    redirect(url_for('login'))
