from django.contrib import admin
from .models import SellerRequest, CustomUser


class UserInline(admin.StackedInline):
    model = CustomUser
    extra = 1
    fields = (
        'username', 'email', 'password', 'phone_number',
        'first_name', 'last_name', 'patronymic', 'avatar',
    )


# class SellerRequestInline(admin.StackedInline):
#     model = SellerRequest
#     extra = 1
#     fields = ('user', 'full_name', 'project_name', 'address')
#
#
# @admin.register(Seller)
# class SellerAdmin(admin.ModelAdmin):
#     list_display = ('user', 'project_name', 'category', 'address')
#     inlines = [SellerRequestInline]

@admin.register(SellerRequest)
class SellerRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'project_name', 'category_id', 'phone_number', 'address')
    inlines = [UserInline]