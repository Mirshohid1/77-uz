from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import re


def validate_phone_number(value):
    pattern = r'^(?:\+998\d{9}|\+7\d{10})$'
    if not re.match(pattern, value):
        raise ValidationError(
            "The phone number must start with '+998' (Uzbekistan) or '+7' (Russia) and contain the correct number of digits."
        )

def path_to_avatar(instance, filename):
    return f"uploads/user_{instance.id}/avatar_{filename}"


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        _("phone number"),
        max_length=15,
        unique=True, blank=True, null=True,
        validators=[validate_phone_number],
    )
    avatar = models.ImageField(upload_to=path_to_avatar, blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"User: {self.username}, {self.email} | {self.phone_number}"