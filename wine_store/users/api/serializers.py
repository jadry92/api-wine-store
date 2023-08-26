# dj_rest_auth
from dj_rest_auth.registration.serializers import RegisterSerializer

# Django
from django.contrib.auth import get_user_model

# Rest Framework
from rest_framework import serializers

# User
from wine_store.users.models import UserAddress, UserPayment

User = get_user_model()


class RegisterSerializerCustom(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"
        read_only_fields = ["user"]


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = "__all__"
        read_only_fields = ["user"]
