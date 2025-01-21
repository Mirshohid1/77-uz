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


def data_format_validate(
        value: str, title=False, capitalize=False,
        required=False, unique=False
):
    """
    Function to validate and format a string based on the given parameters.

    :param value: the string to be validated and formatted.
    :param title: boolean flag indicating if the string should be in title case. If True, the string is formatted with title case.
    :param capitalize: boolean flag indicating if the string should be capitalized. If True, the string is formatted with capitalize case.
    :param required: boolean flag indicating if the string is required. If True and the string is empty, raises a ValidationError.
    :param unique: boolean flag indicating if the string should be unique. If True, the string is converted to lowercase.
    :return: the formatted string.

    Note: It is not recommended to enable both `title` and `capitalize` at the same time.
    """

    if not value.strip() and required:
        raise ValidationError(
            _("This field is required.")
        )

    if title and not unique:
        return value.strip().title()
    elif capitalize and not unique:
        return value.strip().capitalize()
    elif unique:
        return value.strip().lower()
    else:
        return value.strip()
