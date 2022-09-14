import ipdb
from django.urls import reverse
from institutions.models import Institution, InstitutionInfo
from rest_framework.test import APITestCase
from rest_framework.views import Response, status
from reviews.models import Review
from users.models import User
from works.models import Work


class ReviewViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_login_url = reverse("login")

        cls.reviewer_data = {
            "username": "admin",
            "email": "admin@email.com",
            "password": "1234",
            "first_name": "Admin",
            "last_name": "Test",
        }

        cls.reviewer_credentials = {"username": "admin", "password": "1234"}

        cls.user_regular_institution_data = {
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

    def test_post_review(self):
        work_id = self.work_user_with_institution.id
        review_url = reverse("reviews_post", args=[work_id])

        post = {"comments": "New Comment"}

        admin_login: Response = self.client.post(
            self.base_login_url, data=self.reviewer_credentials
        )

        admin_token = admin_login.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")

        response: Response = self.client.post(review_url, data=post)

        expected_return = status.HTTP_201_CREATED
        response_return = response.status_code

        self.assertEqual(expected_return, response_return)

    def test_post_review_wrong(self):
        work_id = self.work_user_with_institution.id

        review_url = reverse("reviews_post", args=[work_id])

        post = {"comments": "New Comment"}

        regular_login: Response = self.client.post(
            self.base_login_url, data=self.user_regular_credentials
        )

        regular_token = regular_login.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {regular_token}")

        response: Response = self.client.post(review_url, data=post)

        expected_return = status.HTTP_403_FORBIDDEN
        response_return = response.status_code

        self.assertEqual(expected_return, response_return)

    def test_update_owner_review(self):
        work_id = self.work_user_with_institution.id
        review_url = reverse("reviews_post", args=[work_id])

        post = {"comments": "New Comment"}

        admin_login: Response = self.client.post(
            self.base_login_url, data=self.reviewer_credentials
        )

        admin_token = admin_login.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")

        response: Response = self.client.post(review_url, data=post)

        review_id = response.data["id"]

        review_patch = reverse("review_update_delete", args=[review_id])

        response_patch: Response = self.client.patch(
            review_patch, data={"comments": "Comments Patched"}
        )

        expected_return = status.HTTP_200_OK
        response_return = response_patch.status_code

        self.assertEqual(expected_return, response_return)

    def test_update_not_owner_review(self):
        work_id = self.work_user_with_institution.id
        review_url = reverse("reviews_post", args=[work_id])

        post = {"comments": "New Comment"}

        admin_login: Response = self.client.post(
            self.base_login_url, data=self.reviewer_credentials
        )

        admin_token = admin_login.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")

        response: Response = self.client.post(review_url, data=post)

        review_id = response.data["id"]

        user_login: Response = self.client.post(
            self.base_login_url, data=self.user_regular_credentials
        )

        user_token = user_login.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user_token}")

        review_patch = reverse("review_update_delete", args=[review_id])

        response_patch: Response = self.client.patch(
            review_patch, data={"comments": "Comments Patched"}
        )

        expected_return = status.HTTP_403_FORBIDDEN
        response_return = response_patch.status_code

        self.assertEqual(expected_return, response_return)

    def test_get_reviews(self):
        work_id = self.work_user_with_institution.id
        review_url = reverse("reviews_post", args=[work_id])
        get_url = reverse("reviews")

        post = {"comments": "New Comment"}

        admin_login: Response = self.client.post(
            self.base_login_url, data=self.reviewer_credentials
        )

        admin_token = admin_login.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")

        response: Response = self.client.post(review_url, data=post)

        response_get: Response = self.client.get(get_url)

        self.assertEqual(len(response_get.data["results"]), 1)
