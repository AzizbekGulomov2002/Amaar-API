from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'phone_number', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                phone_number=validated_data['phone_number'],
                password=validated_data['password'],
                name=validated_data.get('name', '')
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError({"phone_number": "User with this phone number already exists."})


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone_number=data['phone_number'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'name', 'is_active', 'is_staff', 'date_joined', 'company']
