from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from common.models import BaseModel, Address
from common.validators import data_format_validate

from users.models import Seller


def path_to_icon(instance, filename):
    return f"uploads/icons/category_{instance.id}-{filename}"

def path_to_photo(instance, filename):
    return f"uploads/user_{instance.seller.id}/ad_photos/{filename}"


class Category(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    ads_count = models.PositiveIntegerField(verbose_name=_('ads count'))
    icon = models.ImageField(upload_to=path_to_icon, verbose_name=_('icon'))

    def save(self, *args, **kwargs):
        self.name = data_format_validate(self.name, capitalize=True, required=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.ads_count}"

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class SubCategory(BaseModel):
    name = models.CharField(max_length=150, verbose_name=_('name'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='subcategories')

    def save(self, *args, **kwargs):
        self.name = data_format_validate(self.name, capitalize=True, required=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"category: {self.name}, F_category: {self.category.name}"

    class Meta:
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')


class Ad(BaseModel):
    slug = models.TextField()
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(
        max_length=3, verbose_name=_('currency'),
        validators=[MinLengthValidator(3)]
    )
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, related_name='ads', verbose_name=_('sub category')
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, related_name='ads', verbose_name=_('address')
    )
    seller = models.ForeignKey(
        Seller, on_delete=models.SET_NULL, related_name='ads', verbose_name=_('seller')
    )

    def clean(self):
        self.name = data_format_validate(self.name, capitalize=True, required=True)
        self.description = data_format_validate(self.description, capitalize=True, required=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, sub category: {self.sub_category.name}, seller: {self.seller.username}"

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')


class Photo(BaseModel):
    photo = models.ImageField(upload_to=path_to_photo, verbose_name=_('photo'))
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='photos', verbose_name=_('ad')
    )

    def __str__(self):
        return f"{self.photo.name}: {self.photo.url}"

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
