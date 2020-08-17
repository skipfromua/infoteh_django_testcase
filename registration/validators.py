from django.core.validators import ValidationError
from django.contrib.auth import password_validation
from django.core.validators import validate_email
from django.contrib.auth.models import User


def custom_validate_for_empty_spaces(entry):
    if entry:
        return True
    else:
        return False


def custom_validate_username(username):
    user = User.objects.filter(username=username)
    if user:
        return True
    else:
        return False


def custom_validate_email(email):
    try:
        validate_email(email)
    except ValidationError as error_message:
        return error_message


def custom_validate_password(password):
    try:
        password_validation.validate_password(password)
    except ValidationError as error_message:
        return error_message
