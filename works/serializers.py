from asyncore import read
from rest_framework import serializers
from reviews.serializers import ReviewSerializer
from users.serializers import SerializerUsers
from feedbacks.serializers import FeedbackSerializer
import ipdb

from .models import Work


class WorkSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)
    users = SerializerUsers(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "reviews",
            "users",
            "feedbacks",
        ]

    def create(self, validated_data: dict) -> Work:
        user_institution = self.context["request"].user.institution
        user = self.context["request"].user
        # validated_data["users"].set(user)

        # ipdb.set_trace()
        if not user_institution:
            validated_data["visibility"] = "Public"
            new_work = Work.objects.create(**validated_data)
            new_work.users.add(user)
            # user.set(new_work)
            # new_work.set(user)
            new_work.save()
            return new_work

        new_work = Work.objects.create(**validated_data)
        new_work.users.add(user)
        # user.set(new_work)

        # new_work.set(user)
        new_work.save()

        return new_work

    # def update(self, instance: Work, validated_data: dict) -> Work:

    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance
