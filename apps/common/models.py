from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .validators import data_format_validate


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def save(self, *args, **kwargs):
        self.name = data_format_validate(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def save(self, *args, **kwargs):
        self.name = data_format_validate(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def save(self, *args, **kwargs):
        self.name = data_format_validate(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

    def __str__(self):
        return self.name


class Address(BaseModel):
    country = models.OneToOneField(
        Country, on_delete=models.SET_NULL, related_name='address', verbose_name=_('country'),
        null=True, blank=True,
    )
    city = models.OneToOneField(
        City, on_delete=models.SET_NULL, related_name='address', verbose_name=_('city'),
        null=True, blank=True,
    )
    district = models.OneToOneField(
        District, on_delete=models.SET_NULL, related_name='address', verbose_name=_('district'),
        null=True, blank=True,
    )
    street = models.CharField(max_length=100, null=True, blank=True)
    building_number = models.CharField(max_length=10, null=True, blank=True)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    additional_info = models.TextField(blank=True, null=True)

    def get_short_address(self):
        return f"{self.country}, {self.city}, {self.district}"

    def clean(self):
        self.street = data_format_validate(self.street, capitalize=True, required=True)
        self.additional_info = data_format_validate(self.additional_info, capitalize=True, required=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class Page(BaseModel):
    content = models.TextField(verbose_name=_('content'))
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content[:50])
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
