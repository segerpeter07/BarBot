# /barbot/models.py

from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email

from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt, db

class EmailPasswordForm(form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class NewUserForm(form):
    username = StringField('Username', validators[DataRequired()])
    email = StringField('Email', validators[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    height = IntegerField('Height', validators[DataRequired()])
    weight = IntegerField('Weight', validators[DataRequired()])


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    height = db.Column(db.Integer, unique=False)
    weight = db.Column(db.weight, unique=False)
    barcode = db.Column(db.String(64), unique=False)

    @hybrid_property
    def password(self):
        return self.password

    def username(self):
        return self.username

    def email(self):
        return self.email

    def height(self):
        return self.height

    def weight(self):
        return self.weight

    def barcode(self):
        return self.barcode


    @password.setter
    def _set_password(self, plaintext):
        self.password = bcrypt.generate_password_hash(plaintext)


    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
