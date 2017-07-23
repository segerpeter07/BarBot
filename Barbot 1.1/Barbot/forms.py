# /barbot/forms.py

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class EmailPasswordForm(form):
    email = StringField('Email', validators=[DataRequired(), Email(),
        Unique(
            User.email,
            message='There is already an account with that email.')])
    password = PasswordField('Password', validators=[DataRequired()])

class EmailForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
