# /barbot/models.py

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt, db

class EmailPasswordForm(form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    barcode = db.Column(db.String(64), unique=True)

    @hybrid_property
    def password(self):
        return self.password


    @password.setter
    def _set_password(self, plaintext):
        self.password = bcrypt.generate_password_hash(plaintext)


    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
