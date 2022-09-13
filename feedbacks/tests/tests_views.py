from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.views import Response, status
from rest_framework.authtoken.models import Token
from faker import Faker
from feedbacks.models import Feedback
from users.models import User
from works.models import Work

import ipdb

fake = Faker()


class FeedbacksTestViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client: APIClient

        normal_user_data = {
            "username": "anthoni",
            "email": "anthoni@anthoni.com",
            "first_name": "anthoni",
            "last_name": "felipi",
            "password": "1234",
            "degree": "None",
            "about": "None",
        }

        normal_user = User.objects.create_user(**normal_user_data)
        cls.token_normal_user = Token.objects.create(user=normal_user)

        super_user_data = {
            "username": "admin",
            "email": "admin@admin.com",
            "first_name": "admin",
            "last_name": "test",
            "password": "1234",
            "degree": "None",
            "about": "None",
        }

        cls.super_user = User.objects.create_superuser(**super_user_data)
        cls.token_super_user = Token.objects.create(user=cls.super_user)

        cls.work_data = {
            "knowledge_area": "TI",
            "title": "eu sou um trabalho",
            "summary": "eu tenho 5 paginas",
            "link": "Link do trabalho no google drive",
            "visibility": "Public",
        }

        cls.work = Work.objects.create(**cls.work_data)

        cls.feedback_data = {
            "feedback": "Eu sou um feedback",
            "rate": 8,
        }

        cls.feedback_wrong_data = {
            "rate": 8,
        }

        cls.feedback = Feedback.objects.create(
            **cls.feedback_data, work_id=cls.work.id, user_id=cls.super_user.id
        )

        cls.base_url = reverse("feedback", kwargs={"work_id": cls.work.id})
        cls.base_url_details = reverse(
            "feedback_id",
            kwargs={"work_id": cls.work.id, "feedback_id": cls.feedback.id},
        )

    def test_create_feedback_normal_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )

        create_feedback: Response = self.client.post(
            self.base_url,
            self.feedback_data,
        )

        code_response = status.HTTP_201_CREATED
        code_result = create_feedback.status_code

        self.assertEqual(code_response, code_result)

    def test_create_feedback_without_some_fields(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )

        create_feedback: Response = self.client.post(
            self.base_url,
            self.feedback_wrong_data,
        )

        code_response = status.HTTP_400_BAD_REQUEST
        code_result = create_feedback.status_code

        self.assertEqual(code_response, code_result)

    def test_list_feedbacks_with_normal_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )

        list_institutions: Response = self.client.get(self.base_url)

        code_response = status.HTTP_200_OK
        code_result = list_institutions.status_code

        self.assertEqual(code_response, code_result)

    def test_update_feedback_normal_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )

        update: Response = self.client.patch(
            self.base_url_details, data={"feedback": "Agora eu sou um feedback editado"}
        )
        code_response = status.HTTP_200_OK
        code_result = update.status_code

        self.assertEqual(code_response, code_result)

    def test_delete_feedback(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )
        response: Response = self.client.delete(self.base_url_details)

        expected_status_code = status.HTTP_204_NO_CONTENT
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
