# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import User, Company



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",'phone_number', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            name=validated_data.get('name', '')
        )
        return user



class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone_number=data['phone_number'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

# User = get_user_model()
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name', 'email')
#

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'name', 'is_active', 'is_staff', 'date_joined', 'company']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'