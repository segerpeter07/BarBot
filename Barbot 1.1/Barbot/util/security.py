# /barbot/util/security.py

from itsdangerous import URLSafeTimedSerializer
from .. import app

ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
