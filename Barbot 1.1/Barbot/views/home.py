# /barbot/views/home.py

from flask import Blueprint, render_template, url_for

from flask_login import login_user

from . import app, db, cache
from .forms import EmailPasswordForm, EmailForm, PasswordForm
from .util import ts
from .util.email import send_email

home = Blueprint('home', __name__)


@home.route('/')
@cache.cached(timeout=60)   # Homepage is cached every 60 seconds
def index():
    # do some stuff
    return render_template('home/index.html')


@home.route('/about')
def about():
    # do some stuff
    return render_template('home/about.html')


@home.route('/login', methods=["GET", "POST"])
def login():
    # do some stuff
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))
    return render_template('home/login.html', form=form)


@home.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))

@home.route('/signup', methods=['GET', 'POST'])
def signup():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data
            email = form.email.data
            password = form.password.data
            height = form.height.data
            weight = form.weight.data
            barcode = '00000'
        )
        db.session.add(user)
        db.session.commit()

        # Send confimation email with link
        subject = 'Confirm your email'

        token = ts.dumps(self.email, salt='email-confirm-key')

        confirm_url = url_for(
            'confirm_email',
            token = token,
            _external = True)

        html = render_template(
            'email/activate.html',
            confirm_url=confirm_url)

        # send_email() defined in /Barbot/util/email.py
        send_email(user.email, subject, html)

        return redirect(url_for('profile'))

    return render_template('home/signup.html')


@home.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))


@home.route('/reset', methods=['GET', 'POST'])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"

        token = ts.dumps(user.email, salt='recover-key')

        recover_url = url_for(
            'reset_with_token',
            token=token
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        send_email(user.email, subject, html)

        return redirect(url_for('/login'))
    return render_template('reset.html', form=form)


@home.route('reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt='recover-key', max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('reset_with_token.html', form=form, token=token)
