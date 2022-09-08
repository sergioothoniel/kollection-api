from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SerializerUsers(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "degree",
            "about",
            "role",
            "date_joined",
            "is_active",
        ]
        extra_kwargs = {
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Username already exists",
                    )
                ]
            },
            "password": {"write_only": True},
        }

    def get_full_name(self, obj: User) -> str:
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data: dict) -> User:
        new_user = User.objects.create_user(**validated_data)

        new_user.save()

        return new_user

    def update(self, instance: User, validated_data: dict) -> User:

        for key, value in validated_data.items():
            if key == "password":
                value = make_password(value)

            setattr(instance, key, value)
        instance.save()
        return instance


class SerializerLoginJwt(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token["role"] = user.role

        return token
