import ipdb
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import Response, status
from users.models import User


class UserTestView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_login_url = reverse("login")

        cls.base_signin_url = reverse("users")

        cls.superuser_data = {
            "username": "superuser",
            "password": "1234",
            "first_name": "Super",
            "last_name": "User",
        }

        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

        cls.admin = {
            "username": "admin",
            "email": "admin@email.com",
            "password": "1234",
            "first_name": "Admin",
            "last_name": "Test",
            "role": "Admin",
        }

        cls.admin_credentials = {
            "username": "admin",
            "password": "1234",
        }

        cls.superuser_credentials = {
            "username": "superuser",
            "password": "1234",
        }

    def test_account_signin(self):
        response: Response = self.client.post(self.base_signin_url, data=self.admin)
        expected_status_code = status.HTTP_201_CREATED
        result_response_status = response.status_code

        self.assertEqual(expected_status_code, result_response_status)

    def test_account_signin_error(self):
        response: Response = self.client.post(self.base_signin_url, data=self.admin)

        response: Response = self.client.post(self.base_signin_url, data=self.admin)
        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_response_status = response.status_code

        self.assertEqual(expected_status_code, result_response_status)

    def test_account_login(self):
        create_user: Response = self.client.post(self.base_signin_url, data=self.admin)

        login_user: Response = self.client.post(
            self.base_login_url, data=self.admin_credentials
        )

        user_id = create_user.data["id"]

        user_token = login_user.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")

        base_user_id_url = reverse("user_id", args=[user_id])

        response: Response = self.client.get(base_user_id_url)

        expected_status_code = status.HTTP_200_OK

        result_response_status = response.status_code

        self.assertEqual(expected_status_code, result_response_status)

    def test_account_patch(self):
        login_superuser: Response = self.client.post(
            self.base_login_url, data=self.superuser_credentials
        )

        admin_user: Response = self.client.post(self.base_signin_url, data=self.admin)

        superuser_token = login_superuser.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {superuser_token}")

        user_id = admin_user.data["id"]

        base_user_id_url = reverse("user_admin", args=[user_id])

        response: Response = self.client.patch(base_user_id_url, data={"role": "Admin"})

        expected_status_code = status.HTTP_200_OK
        result_response_status = response.status_code

        self.assertEqual(expected_status_code, result_response_status)
        self.assertEqual(response.data["role"], "Admin")

