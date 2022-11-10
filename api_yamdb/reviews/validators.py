import re

from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from datetime import datetime


class UsernameRegexValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя."""

    regex = r'^[\w.@+-]+\Z'
    flags = 0
    message = ('Не допустимые символы <{value}> в нике',
               'Набор символов не более 150'
               'Только буквы, цифры и @/./+/-/_')


def username_me(value):
    """Проверка имени пользователя (me недопустимое имя)."""
    if value == 'me':
        raise ValidationError(
            'Имя пользователя "me" не разрешено.'
        )
    return value


def validate_year(value):
    if value >= datetime.now().year:
        raise ValidationError(
            message=f'Год {value} больше текущего!',
            params={'value': value},
        )
