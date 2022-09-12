import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    REGULAR = "Regular"
    ADMIN = "Admin"
    REVIEWER = "Reviewer"


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=127, unique=True)
    email = models.EmailField(max_length=127, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=15,
        choices=Roles.choices,
        default=Roles.REGULAR,
    )
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    institution = models.ForeignKey(
        "institutions.Institution",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="users",
    )

    works = models.ManyToManyField("works.Work", related_name="users")
