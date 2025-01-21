from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from common.validators import validate_phone_number, data_format_validate


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

    def clean(self):
        self.first_name = data_format_validate(self.first_name, is_name=True)
        self.last_name = data_format_validate(self.last_name, is_name=True)
        self.phone_number = data_format_validate(self.phone_number, unique=True, required=True)
        self.email = data_format_validate(self.email, unique=True, required=True)
        self.username = data_format_validate(self.username, unique=True, required=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"User: {self.username}, {self.email} | {self.phone_number}"

class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=100)
    category = models.ForeignKey('store.Category', on_delete=models.CASCADE, related_name='sellers')
    address = models.ForeignKey('common.Address', on_delete=models.SET_NULL, related_name='sellers')

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name} {self.patronymic}"
