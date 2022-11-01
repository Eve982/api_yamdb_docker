import re
from django.core.exceptions import ValidationError
from datetime import datetime


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )


def validate_year(value):
    if datetime.now().year < value:
        raise ValidationError(
            message='Год %(value)s больше текущего!',
            params={'value': value},
        )
