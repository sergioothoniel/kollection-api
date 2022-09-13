from rest_framework import serializers

from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

from institutions.serializers import InstitutionSerializer


class SerializerGetUsers(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    institution = InstitutionSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "degree",
            "about",
            "role",
            "is_active",
            "institution",
        ]
        read_only_fields = [
            "is_active",
            "role",
        ]

    def get_full_name(self, obj: User) -> str:
        return f"{obj.first_name} {obj.last_name}"


class SerializerUsers(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    institution = InstitutionSerializer(read_only=True)

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
            "institution",
        ]

        read_only_fields = [
            "is_active",
            "role",
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


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    institution = InstitutionSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "degree",
            "about",
            "role",
            "date_joined",
            "is_active",
            "institution",
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
        }

    def get_full_name(self, obj: User) -> str:
        return f"{obj.first_name} {obj.last_name}"
