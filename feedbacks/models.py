from django.db import models
import uuid

class feedbacks(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
  feedback = models.CharField(max_length=200, blank=False)
  rate = models.IntegerField()

  work = models.ForeignKey("works.Work", related_name="feedbacks", on_delete=models.CASCADE)
  user = models.ForeignKey("users.User", related_name="feedbacks", on_delete=models.CASCADE)