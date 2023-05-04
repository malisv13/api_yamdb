import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Недопустимый username'),
            params={'value': value},
        )
    reg = r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$'
    if re.match(reg, value) is None:
        raise ValidationError(
            (f'Недопустимые символы <{value}> в username.'),
            params={'value': value},
        )
