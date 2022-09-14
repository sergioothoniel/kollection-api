from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.views import Response, status
from works.models import Work
from users.models import User
from rest_framework.authtoken.models import Token
from faker import Faker

fake = Faker()


class WorkTestView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client: APIClient

        cls.work_info_data = {
            "knowledge_area": "Tecnologia",
            "title": "Aprenda a programar",
            "summary": "testing",
            "link": "http://test.com.br",
            "visibility": "Intern",
            "is_reviewed": True,
            "is_active": True,
        }
        cls.work_info = Work.objects.create(**cls.work_info_data)

        cls.work_data = {"name": fake.name()}
        cls.work_data_update = {"name": fake.name()}

        cls.work = Work.objects.create(
            **cls.work_data_update, infos_id=cls.work_info.id
        )

        normal_user_data = {
            "username": fake.name(),
            "email": fake.email(),
            "first_name": fake.name(),
            "last_name": fake.name(),
            "password": fake.password(),
            "degree": "None",
            "about": "None",
        }

        normal_user = User.objects.create_user(**normal_user_data)
        cls.token_normal_user = Token.objects.create(user=normal_user)

        cls.base_url = reverse("works")
        cls.base_url_details = reverse("work_id", kwargs={"work_id": cls.work.id})

    def test_create_work_super_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_super_user.key)

        create_work: Response = self.client.post(self.base_url, self.work_data)

        code_response = status.HTTP_201_CREATED
        code_result = create_work.status_code

        self.assertEqual(code_response, code_result)

    def test_create_work_normal_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )
        create_work: Response = self.client.post(self.base_url, self.work_data)
        code_response = status.HTTP_403_FORBIDDEN
        code_result = create_work.status_code

        self.assertEqual(code_response, code_result)

    def test_update_work_super_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_super_user.key)

        update: Response = self.client.patch(
            self.base_url_details, data={"title": "Kenzie Academy"}
        )
        code_response = status.HTTP_200_OK
        code_result = update.status_code

        self.assertEqual(code_response, code_result)

    def test_list_works_with_normal_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )

        list_works: Response = self.client.get(self.base_url_details)

        code_response = status.HTTP_403_FORBIDDEN
        code_result = list_works.status_code

        self.assertEqual(code_response, code_result)

    def test_delete_work(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_super_user.key)
        response: Response = self.client.delete(self.base_url_details)

        expected_status_code = status.HTTP_204_NO_CONTENT
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
