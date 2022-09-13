from feedbacks.serializers import FeedbackSerializer
from rest_framework import serializers
from reviews.serializers import ReviewSerializer
from users.serializers import SerializerUsers

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

        if not user_institution:
            validated_data["visibility"] = "Public"
            new_work = Work.objects.create(**validated_data)
            new_work.users.add(user)

            new_work.save()
            return new_work

        new_work = Work.objects.create(**validated_data)
        new_work.users.add(user)

        new_work.save()

        return new_work
