import ipdb
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.serializers import SerializerGetUsers
from works.models import Work
from works.serializers import WorkSerializer

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = SerializerGetUsers(read_only=True)
    works = WorkSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "comments",
            "user",
            "works",
        ]
        read_only_fields = ["user", "works"]

    def create(self, validated_data):
        work_id = self.context["view"].kwargs["work_id"]
        users = self.context["request"].user

        work = get_object_or_404(Work, id=work_id)

        validated_data["works"] = work
        validated_data["user"] = users

        if work.reviews.filter(user=users).exists():
            raise serializers.ValidationError(
                {"detail": "You have already reviewed this Work."}
            )

        work.is_reviewed = True
        work.save()

        return Review.objects.create(**validated_data)
