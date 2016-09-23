from django.core.exceptions import ValidationError


def validate_integer_placeholder(value):
    try:
        value % 0
    except (TypeError, ValueError) as e:
        raise ValidationError(str(e))


def validate_str_placeholder(value):
    try:
        value % "str"
    except (TypeError, ValueError) as e:
        raise ValidationError(str(e))
