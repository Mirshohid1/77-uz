from rest_framework import serializers
from django.core.validators import ValidationError as DjangoValidationError
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from common.validators import validate_phone_number
from store.models import Category

from .models import CustomUser, Seller, SellerRequest


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create(**validated_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return user

class RegisterSellerSerializer(serializers.Serializer):
    class Meta:
        fields = ('full_name', 'project_name', 'category_id', 'phone_number', 'address')

    def validate_phone_number(self, value):
        try:
            validate_phone_number(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return value

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("The category with this ID was not found.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return SellerRequest.objects.create(**validated_data)
