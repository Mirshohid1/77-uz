from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from common.validators import data_format_validate


def path_to_icon(instance, filename):
    return f"uploads/icons/category_{instance.id}-{filename}"


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
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

