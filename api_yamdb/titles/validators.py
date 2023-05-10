from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            (f"{value} - неправильный год!"),
            params={'value': value},
        )
