import ipdb
from django.test import TestCase
from institutions.models import Institution, InstitutionInfo
from reviews.models import Review
from users.models import User
from works.models import Work


class ReviewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.reviewer_data = {
            "username": "admin",
            "email": "admin@email.com",
            "password": "1234",
            "first_name": "Admin",
            "last_name": "Test",
        }

        cls.user_regular_institution_data = {
            "username": "regular",
            "email": "regular@email.com",
            "password": "1234",
            "first_name": "Regular",
            "last_name": "Test",
        }

        cls.user_regular_data_no_institution = {
            "username": "regularnoinstitution",
            "email": "regularnoinstitution@email.com",
            "password": "1234",
            "first_name": "Regular",
            "last_name": "Test",
        }

        cls.institution_info_data = {
            "city": "Curitiba",
            "state": "Paraná",
            "link": "https://kenzie.com.br/",
            "phone": "4199999999",
            "cep": "81400000",
        }

        cls.user_work_with_institution_data = {
            "knowledge_area": "T.I Test",
            "title": "My First Work",
            "link": "Fake Link",
        }

        cls.user_work_without_institution_data = {
            "knowledge_area": "T.I Test 2",
            "title": "My First Work - No Institution",
            "link": "Fake Link",
        }

        cls.institution_info = InstitutionInfo.objects.create(
            **cls.institution_info_data
        )

        cls.institution = Institution.objects.create(
            name="Institution Test", infos=cls.institution_info
        )

        cls.reviewer = User.objects.create_user(**cls.reviewer_data, role="Reviewer")

        cls.user_with_institution = User.objects.create_user(
            **cls.user_regular_institution_data, institution=cls.institution
        )

        cls.user_without_institution = User.objects.create_user(
            **cls.user_regular_data_no_institution
        )

        cls.work_user_with_institution = Work.objects.create(
            **cls.user_work_with_institution_data
        )

        cls.user_with_institution.works.add(cls.work_user_with_institution)

    def test_create_review(self):
        review = Review.objects.create(
            comments="New Comment",
            user=self.user_with_institution,
            works=self.work_user_with_institution,
        )

        self.assertEqual(type(review.comments), str)
        self.assertEqual(review.comments, "New Comment")

    def test_relation_review(self):
        review = Review.objects.create(
            comments="New Comment",
            user=self.user_with_institution,
            works=self.work_user_with_institution,
        )

        self.assertEqual(review.user, self.user_with_institution)
        self.assertEqual(review.works, self.work_user_with_institution)
