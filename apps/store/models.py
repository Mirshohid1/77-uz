from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

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
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='subcategories',
        null=True, blank=True,
    )

    def save(self, *args, **kwargs):
        self.name = data_format_validate(self.name, capitalize=True, required=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"category: {self.name}, F_category: {self.category.name}"

    class Meta:
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')


class Ad(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(
        max_length=3, verbose_name=_('currency'),
        validators=[MinLengthValidator(3)]
    )
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, related_name='ads', verbose_name=_('sub category'),
        null=True, blank=True,
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, related_name='ads', verbose_name=_('address'),
        null=True, blank=True,
    )
    seller = models.ForeignKey(
        Seller, on_delete=models.SET_NULL, related_name='ads', verbose_name=_('seller'),
        null=True, blank=True,
    )

    def clean(self):
        self.name = data_format_validate(self.name, capitalize=True, required=True)
        self.description = data_format_validate(self.description, capitalize=True, required=True)
        if not self.slug:
            slug = slugify(self.name)
            self.slug = f"{slug}-77"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, sub category: {self.sub_category.name}, seller: {self.seller.username}"

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')


class AdExtraInfo(models.Model):
    STATUS_CHOICES = [
        ('in_moderation', 'In Moderation'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('expired', 'Expired')
    ]

    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, related_name='ad_extra', verbose_name=_('ad'))
    status = models.CharField(max_length=14, default='in_moderation', verbose_name=_('status'))
    expires_at = models.DateTimeField(verbose_name=_('expires at'))

    class Meta:
        verbose_name = _('Ad Extra Info')
        verbose_name_plural = _("Ad Extra Infos")


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
