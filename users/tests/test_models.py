import ipdb
from django.db import IntegrityError
from django.test import TestCase
from institutions.models import Institution
from django.urls import reverse
from users.models import User
from model_bakery import baker
class UserModelTest(TestCase):
    
    @classmethod
    def setUp(cls):
        cls.user = baker.make_recipe('users.create_user')
    def test_student_max_length_attributes(self):
        max_length_username = self.user._meta.get_field("username").max_length
        max_length_first_name = self.user._meta.get_field("first_name").max_length
        max_length_last_name = self.user._meta.get_field("last_name").max_length
        self.assertEqual(max_length_username, 127)
        self.assertEqual(max_length_first_name, 50)
        self.assertEqual(max_length_last_name, 50)
    