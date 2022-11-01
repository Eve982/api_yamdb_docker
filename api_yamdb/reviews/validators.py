from django.core.exceptions import ValidationError
from datetime import datetime


def validate_year(value):
    if datetime.now().year < value:
        raise ValidationError(
            message='Год %(value)s больше текущего!',
            params={'value': value},
        )
