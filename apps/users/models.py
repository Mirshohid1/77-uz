from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from common.validators import validate_phone_number, data_format_validate
from common.models import BaseModel, Address


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
    avatar = models.ImageField(upload_to=path_to_avatar, blank=True, null=True, verbose_name=_('avatar'))

    def clean(self):
        self.first_name = data_format_validate(self.first_name, title=True)
        self.last_name = data_format_validate(self.last_name, title=True)
        self.phone_number = data_format_validate(self.phone_number, unique=True, required=True)
        self.email = data_format_validate(self.email, unique=True, required=True)
        self.username = data_format_validate(self.username, unique=True, required=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"User: {self.username}, {self.email} | {self.phone_number}"

class Seller(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE,
        related_name='seller_profile', verbose_name=_('user')
    )
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('patronymic'))
    project_name = models.CharField(max_length=100, verbose_name=_('project name'))
    category = models.ForeignKey(
        'store.Category', on_delete=models.CASCADE, related_name='sellers', verbose_name=_('category')
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, related_name='sellers', verbose_name=_('address'),
        null=True, blank=True,
    )

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name} {self.patronymic}"

    def clean(self):
        self.patronymic = data_format_validate(self.patronymic, title=True)
        self.project_name = data_format_validate(self.project_name, required=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SellerRequest(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller requests', verbose_name=_('User'))
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    project_name = models.CharField(max_length=255, verbose_name=_("Project Name"))
    category_id = models.PositiveIntegerField(verbose_name=_("Category"))
    phone_number = models.CharField(max_length=15, verbose_name=_("Phone Number"), validators=[validate_phone_number])
    address = models.TextField(verbose_name=_("Address"))
    email = models.EmailField(verbose_name=_("Email"))

    class Meta:
        verbose_name = _("Seller Request")
        verbose_name_plural = _("Seller Requests")

    def __str__(self):
        return f"{self.full_name}, {self.project_name}"