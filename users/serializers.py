import ipdb
from django.contrib.auth.hashers import make_password
from institutions.serializers import InstitutionSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


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

    def create(self, validated_data: dict) -> User:
        # ipdb.set_trace()
        if validated_data.get("institution") == "":
            validated_data.pop("institution")
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

    def get_full_name(self, obj: User) -> str:
        # ipdb.set_trace()
        # if obj["institution"]:
        #     return f"{obj.first_name} {obj.last_name}"

        # first_name = obj["first_name"]
        # last_name = obj["last_name"]
        return f"{obj.first_name} {obj.last_name}"


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
