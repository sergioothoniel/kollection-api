from asyncore import read
from rest_framework import serializers
from reviews.serializer import ReviewSerializer

from .models import Work


class WorkSerializer(serializers.ModelSerializer):

    review = ReviewSerializer(many=True)

    class Meta:
        model = Work
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "review"]

    # def create(self, validated_data: dict) -> Work:
    #     new_work = Work.objects.create(**validated_data)

    #     new_work.save()

    #     return new_work

    # def update(self, instance: Work, validated_data: dict) -> Work:

    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance
