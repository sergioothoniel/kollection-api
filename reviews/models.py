import uuid

from django.db import models


class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    comments = models.TextField()

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    works = models.ForeignKey(
        "works.Work", on_delete=models.CASCADE, related_name="reviews"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f"<Review - Name: {self.user.first_name} - Role: {self.user.role}>"
