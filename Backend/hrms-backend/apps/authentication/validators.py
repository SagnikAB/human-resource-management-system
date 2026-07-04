import re
from django.core.exceptions import ValidationError


def validate_strong_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one number.')
    if not re.search(r'[^A-Za-z0-9]', value):
        raise ValidationError('Password must contain at least one special character.')
