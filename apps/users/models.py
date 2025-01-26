from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError

from common.validators import validate_phone_number, data_format_validate, category_exist_validator
from common.models import BaseModel, Address



def path_to_avatar(instance, filename):
    return f"uploads/user_{instance.id}/avatar_{filename}"


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model, providing methods to create
    superusers and regular users with specific roles.

    Methods:
        create_superuser(username, email, password, **extra_fields):
            Creates and returns a superuser with the specified credentials.

        create_user(username, email, password, **extra_fields):
            Creates and returns a regular user with the specified credentials.

        _create_user(username, email, password, **extra_fields):
            Helper method to create and save a user with the given credentials.
       """

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and returns a superuser with the 'admin' role and appropriate flags.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self._create_user(username, email, password, **extra_fields)

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and returns a regular user with the 'user' role.
        """

        extra_fields.setdefault('role', 'user')
        return self._create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        """
        Helper method to create and save a user with the given credentials.
        Validates the email and sets the password before saving the user to the database.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class SellerRequest(BaseModel):
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    project_name = models.CharField(max_length=255, verbose_name=_("Project Name"))
    category_id = models.PositiveIntegerField(verbose_name=_("Category"), validators=[category_exist_validator])
    phone_number = models.CharField(max_length=15, verbose_name=_("Phone Number"), validators=[validate_phone_number])
    address = models.TextField(verbose_name=_("Address"))

    class Meta:
        verbose_name = _("Seller Request")
        verbose_name_plural = _("Seller Requests")

    def __str__(self):
        return f"{self.full_name}, {self.project_name}"


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('user', 'User')
    ]

    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        _("phone number"),
        max_length=15,
        unique=True, blank=True, null=True,
        validators=[validate_phone_number],
    )
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('patronymic'))
    category = models.ForeignKey('store.Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    avatar = models.ImageField(upload_to=path_to_avatar, blank=True, null=True, verbose_name=_('avatar'))
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name=_('Role'),
    )
    seller_request = models.OneToOneField(
        SellerRequest, on_delete=models.SET_NULL,
        related_name='user', verbose_name=_('seller request'),
        null=True, blank=True
    )

    objects = CustomUserManager()

    def clean(self):
        if self.username:
            self.username = data_format_validate(str(self.username), unique=True)
        if self.email:
            self.email = data_format_validate(str(self.email), unique=True)
        if self.first_name:
            self.first_name = data_format_validate(str(self.first_name), title=True)
        if self.last_name:
            self.last_name = data_format_validate(str(self.last_name), title=True)
        if self.phone_number:
            self.phone_number = data_format_validate(str(self.phone_number), unique=True, required=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"id: {self.id}: {self.username}, {self.email} | {self.phone_number}"
