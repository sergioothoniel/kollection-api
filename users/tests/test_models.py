import ipdb
from django.db import IntegrityError
from django.test import TestCase
from institutions.models import Institution
from users.models import User
from .mock import superuser, manager, reviewer_user, institution, student


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.institution = Institution.objects.create(**institution)
        cls.superuser = User.objects.create_superuser(**superuser)
        cls.manager = User.objects.create(**manager,institution=cls.institution)
        cls.reviewer_user = User.objects.create_user(**reviewer_user, institution=cls.institution)
        cls.student = User.objects.create_user(**student, institution=cls.institution)

    def test_student_max_length_attributes(self):
        max_length_username = self.student._meta.get_field("username").max_length
        max_length_first_name = self.student._meta.get_field("first_name").max_length
        max_length_last_name = self.student._meta.get_field("last_name").max_length
        self.assertEqual(max_length_username, 127)
        self.assertEqual(max_length_first_name, 50)
        self.assertEqual(max_length_last_name, 50)

    def test_student_same_name(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**student, institution=self.institution)

    def test_student_has_information_fields(self):
        self.assertEqual(self.student.username, student["username"])
        self.assertEqual(self.student.first_name, student["first_name"])
        self.assertEqual(self.student.last_name, student["last_name"])
        self.assertEqual(self.student.is_superuser, student["is_manager"])
        self.assertEqual(self.student.is_reviewer, student["is_reviewer"])
        self.assertEqual(self.student.is_student, student["is_student"])

    def test_student_is_active_default_true(self):
        default_student = self.student._meta.get_field("is_active").default
        default_reviewer_user = self.reviewer_user._meta.get_field("is_active").default
        default_superuser = self.superuser._meta.get_field("is_active").default
        default_manager = self.manager._meta.get_field("is_active").default
        self.assertTrue(default_student)
        self.assertTrue(default_reviewer_user)
        self.assertTrue(default_superuser)
        self.assertTrue(default_manager)

    def test_student_attach_store_correctly(self):
        self.assertEqual(self.student.institution, self.institution)