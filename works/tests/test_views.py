import ipdb
from django.urls import reverse
from institutions.models import Institution, InstitutionInfo
from rest_framework.test import APITestCase
from rest_framework.views import Response, status
from users.models import User
from works.models import Work


class WorkTestView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_login_url = reverse("login")
        cls.work_post_get_url = reverse("works")
        # cls.work_details = reverse("work_detail")

        cls.user_regular = {
            "username": "regular",
            "email": "regular@email.com",
            "password": "1234",
            "first_name": "Regular",
            "last_name": "Test",
        }

        cls.user_regular_credentials = {"username": "regular", "password": "1234"}

        cls.user_regular_data_no_institution = {
            "username": "regularnoinstitution",
            "email": "regularnoinstitution@email.com",
            "password": "1234",
            "first_name": "Regular",
            "last_name": "Test",
        }
        cls.user_regular_no_institution_credentials = {
            "username": "regularnoinstitution",
            "password": "1234",
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

        cls.user_with_institution = User.objects.create_user(
            **cls.user_regular, institution=cls.institution
        )

        cls.user_without_institution = User.objects.create_user(
            **cls.user_regular_data_no_institution
        )

        cls.work_user_with_institution = Work.objects.create(
            **cls.user_work_with_institution_data
        )

        cls.work_user_without_institution = Work.objects.create(
            **cls.user_work_without_institution_data, visibility="Public"
        )

        cls.user_with_institution.works.add(cls.work_user_with_institution)

        cls.user_without_institution.works.add(cls.work_user_without_institution)

    def test_create_work_user_with_institution(self):
        user_regular_response: Response = self.client.post(
            self.base_login_url, data=self.user_regular_credentials
        )
        user_token = user_regular_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")

        create_work: Response = self.client.post(
            self.work_post_get_url, data=self.user_work_with_institution_data
        )

        code_response = status.HTTP_201_CREATED
        code_result = create_work.status_code

        self.assertEqual(code_response, code_result)
        self.assertEqual(create_work.data["visibility"], "Intern")

    def test_create_work_user_without_institution(self):
        user_regular_no_institution_response: Response = self.client.post(
            self.base_login_url, data=self.user_regular_no_institution_credentials
        )
        user_no_institution_token = user_regular_no_institution_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_no_institution_token}")

        create_work: Response = self.client.post(
            self.work_post_get_url, data=self.user_work_without_institution_data
        )

        code_response = status.HTTP_201_CREATED
        code_result = create_work.status_code

        self.assertEqual(code_response, code_result)
        self.assertEqual(create_work.data["visibility"], "Public")

    def test_list_works_with_normal_user(self):
        user_regular_response: Response = self.client.post(
            self.base_login_url, data=self.user_regular_credentials
        )
        user_token = user_regular_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")

        list_works: Response = self.client.get(self.work_post_get_url)

        list_count = 2
        list_response_count = list_works.data["count"]
        code_response = status.HTTP_200_OK
        code_result = list_works.status_code

        self.assertEqual(list_response_count, list_count)
        self.assertEqual(code_response, code_result)

    def test_list_works_with_normal_user_no_institution(self):
        user_regular_response: Response = self.client.post(
            self.base_login_url, data=self.user_regular_no_institution_credentials
        )
        user_token = user_regular_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")

        list_works: Response = self.client.get(self.work_post_get_url)

        list_count = 1
        list_response_count = list_works.data["count"]
        code_response = status.HTTP_200_OK
        code_result = list_works.status_code

        self.assertEqual(list_response_count, list_count)
        self.assertEqual(code_response, code_result)

    def test_delete_work_owner(self):
        delete_url = reverse("work_detail", args=[self.work_user_with_institution.id])
        user_regular_response: Response = self.client.post(
            self.base_login_url, data=self.user_regular_credentials
        )
        user_token = user_regular_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")

        response_delete: Response = self.client.delete(delete_url)

        code_response = status.HTTP_204_NO_CONTENT
        code_result = response_delete.status_code

        self.assertEqual(code_response, code_result)

    def test_delete_work_not_owner(self):
        delete_url = reverse("work_detail", args=[self.work_user_with_institution.id])
        user_regular_response: Response = self.client.post(
            self.base_login_url, data=self.user_regular_no_institution_credentials
        )
        user_token = user_regular_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")

        response_delete: Response = self.client.delete(delete_url)

        code_response = status.HTTP_403_FORBIDDEN
        code_result = response_delete.status_code

        self.assertEqual(code_response, code_result)
