from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

import re


def validate_phone_number(value):
    """
    Validates a phone number format.
    - Uzbekistan: +998 followed by 9 digits.
    - Russia: +7 followed by 10 digits.
    """
    pattern = r'^(?:\+998\d{9}|\+7\d{10})$'
    if not re.match(pattern, value):
        raise ValidationError(
            _("The phone number must start with '+998' (Uzbekistan) or '+7' (Russia) and contain the correct number of digits.")
        )


def data_format_validate(value, title=False, capitalize=False, required=False, unique=False):
    """
    Function to validate and format a string based on the given parameters.

    :param value: the string to be validated and formatted.
    :param title: boolean flag indicating if the string should be in title case.
    :param capitalize: boolean flag indicating if the string should be capitalized.
    :param required: boolean flag indicating if the string is required.
    :param unique: boolean flag indicating if the string should be unique (lowercase).
    :return: the formatted string.
    """
    if value is None:
        if required:
            raise ValidationError(_("This field is required and must be a valid string."))
        return None

    if not isinstance(value, str):
        value = str(value)

    value = value.strip()

    if not value and required:
        raise ValidationError(_("This field is required."))

    if title and not unique:
        return value.title()
    elif capitalize and not unique:
        return value.capitalize()
    elif unique:
        return value.lower()
    return value


def category_exist_validator(value):
    from store.models import Category
    if not Category.objects.filter(id=value).exists():
        raise ValidationError("Category not exists")
    return value