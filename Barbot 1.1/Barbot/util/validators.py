# /barbot/util/validators.py

from wtforms.validators import ValidationError

class Unique(object):
    def __init__(self, model, field, message=u'This element already exists'):
        self.model = model
        self.field = field

    def __call__(self, form, field):
        check = self.model.query.filter(self.filter == field.data).first()
        if check:
            raise ValidationError(self.message)
