from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.views import Response, status
from institutions.models import Institution, InstitutionInfo
from users.models import User
from rest_framework.authtoken.models import Token
import ipdb
from faker import Faker

fake = Faker()


class InstitutionTestView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client: APIClient

        cls.institution_info_data = {
            "city": "Curitiba",
            "state": "Paraná",
            "link": "https://kenzie.com.br/",
            "phone": "4199999999",
            "cep": "81400000",
        }
        cls.institution_info = InstitutionInfo.objects.create(
            **cls.institution_info_data
        )

        cls.institution_data = {
            "name": fake.name(),
        }

        cls.institution_data_update = {
            "name": fake.name(),
        }

        cls.institution = Institution.objects.create(
            **cls.institution_data_update, infos_id=cls.institution_info.id
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

        super_user_data = {
            "username": fake.name(),
            "email": fake.email(),
            "first_name": fake.name(),
            "last_name": fake.name(),
            "password": fake.password(),
            "degree": "None",
            "about": "None",
        }

        super_user = User.objects.create_superuser(**super_user_data)
        cls.token_super_user = Token.objects.create(user=super_user)

        cls.base_url = reverse("institutions")
        cls.base_url_details = reverse(
            "institutions_id", kwargs={"institution_id": cls.institution.id}
        )

    def test_create_institution_super_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_super_user.key)

        create_institution: Response = self.client.post(
            self.base_url, self.institution_data
        )

        code_response = status.HTTP_201_CREATED
        code_result = create_institution.status_code

        self.assertEqual(code_response, code_result)

    def test_create_institutiton_normal_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )
        create_institution: Response = self.client.post(
            self.base_url, self.institution_data
        )
        code_response = status.HTTP_403_FORBIDDEN
        code_result = create_institution.status_code

        self.assertEqual(code_response, code_result)

    def test_create_institution_without_name(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_super_user.key)

        test_create = self.client.post(self.base_url, data={})

        code_response = status.HTTP_400_BAD_REQUEST
        code_result = test_create.status_code

        self.assertEqual(code_response, code_result)

    def test_update_institution_super_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_super_user.key)

        update: Response = self.client.patch(
            self.base_url_details, data={"name": "Kenzie Academy"}
        )
        code_response = status.HTTP_200_OK
        code_result = update.status_code

        self.assertEqual(code_response, code_result)

    def test_list_institutions_with_normal_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_normal_user.key
        )

        list_institutions: Response = self.client.get(self.base_url_details)

        code_response = status.HTTP_403_FORBIDDEN
        code_result = list_institutions.status_code

        self.assertEqual(code_response, code_result)

    def test_delete_institution(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_super_user.key)
        response: Response = self.client.delete(self.base_url_details)

        expected_status_code = status.HTTP_204_NO_CONTENT
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
