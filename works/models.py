from django.db import models
import uuid


class Visibilities(models.TextChoices):
    INTERN = "Intern"
    PUBLIC = "Public"


class Work(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    knowledge_area = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    summary = models.TextField(null=True)
    link = models.CharField(max_length=200)
    visibility = models.CharField(
        max_length=15,
        choices=Visibilities.choices,
        default=Visibilities.INTERN,
    )
    is_reviewed = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
