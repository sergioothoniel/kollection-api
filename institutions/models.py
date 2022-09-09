from django.db import models
import uuid


class InstitutionInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    city = models.CharField(max_length=80, blank=True, null=True)
    state = models.CharField(max_length=80, blank=True, null=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=80, blank=True, null=True)
    cep = models.CharField(max_length=80, blank=True, null=True)
   


class Institution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=225, unique=True)

    infos = models.OneToOneField(InstitutionInfo, on_delete=models.CASCADE, related_name='institution')


