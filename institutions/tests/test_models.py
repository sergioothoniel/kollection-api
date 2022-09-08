import ipdb
from django.db import IntegrityError
from django.test import TestCase
from institutions.models import Institution
from users.models import User
from .mock import institution


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.institution = Institution.objects.create(**institution)
        

    def test_institution_max_length_attributes(self):
        max_length_name = self.institution._meta.get_field("name").max_length
        max_length_city = self.institution._meta.get_field("city").max_length
        max_length_state = self.institution._meta.get_field("state").max_length
        max_length_link = self.institution._meta.get_field("link").max_length
        max_length_phone = self.institution._meta.get_field("phone").max_length
        max_length_cep = self.institution._meta.get_field("cep").max_length
        
        self.assertEqual(max_length_name, 225)
        self.assertEqual(max_length_city, 80)
        self.assertEqual(max_length_state, 80)
        self.assertEqual(max_length_link, 250)
        self.assertEqual(max_length_phone, 80)
        self.assertEqual(max_length_cep, 80)
