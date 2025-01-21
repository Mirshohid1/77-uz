from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    street = models.CharField(max_length=100, null=True, blank=True)
    building_number = models.CharField(max_length=10, null=True, blank=True)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    additional_info = models.TextField(blank=True, null=True)

    def get_short_address(self):
        return f"{self.country}, {self.city}, {self.district}"