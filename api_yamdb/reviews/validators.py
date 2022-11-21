from django.core.exceptions import ValidationError
import datetime

now_year = datetime.date.today().year


def validate_not_future(value):
    if value > now_year:
        raise ValidationError('Необходимо указать год не более текущего!')
