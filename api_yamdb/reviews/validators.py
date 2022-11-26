import datetime

from django.core.exceptions import ValidationError

present_year = datetime.date.today().year


def validate_not_future(value):
    if value > present_year:
        raise ValidationError('Необходимо указать год не более текущего!')
