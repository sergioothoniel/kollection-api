import ipdb
from django.db import IntegrityError
from django.test import TestCase
from institutions.models import Institution
from users.models import User

from .mock import institution
from model_bakery import baker

class InstitutionTestModel(TestCase):
    
    @classmethod
    def setUp(cls):
       cls.institution = baker.make('institutions.Institution')



