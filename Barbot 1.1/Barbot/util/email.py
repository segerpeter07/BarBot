# /barbot/util/email.pu

""" This file provides functions for sending emails such as
transactional emails to rest passwords, verify accounts, etc """

from flask import Flask
from flask_mail import Mail

from ..__init__ import app
from ...config import MAIL

mail = Mail(app)

def send_email(address, subject, html):
    # Change sender to MAIL_DEFAULT_SENDER
    msg = Message(subject, sender="do_not_reply@thebarbot.com",
                  recipients=[address])
    msg.html = html
    mail.send(msg)
