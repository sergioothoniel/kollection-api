from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Roles(models.TextChoices):
    STUDENT = "Student"
    ADMIN = "Admin"
    PROFESSOR = "Professor"


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=127, unique=True)
    email = models.EmailField(max_length=127, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    degree = models.CharField(max_length=50)
    about = models.TextField()
    role = models.CharField(
        max_length=15,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "role",
    ]

    institutions = models.ForeignKey(
        "institutions.Institution",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="users",
    )

    works = models.ManyToManyField("works.Work", related_name="users")
