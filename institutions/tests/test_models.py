import ipdb

from django.db import IntegrityError

from django.test import TestCase
from institutions.models import Institution
from users.models import User

from model_bakery import baker


class InstitutionTestModel(TestCase):
    @classmethod
    def setUp(cls):
        cls.institution_info = baker.make_recipe("institutions.institution_info_test")
        cls.institution = baker.make_recipe(
            "institutions.institution_test", infos_id=cls.institution_info.id
        )

    def test_fields_institution(self):
        self.assertIs(self.institution.name, "Kenzie")
        self.assertIs(self.institution.infos_id, self.institution_info.id)

    def tests_fields_institution_infos(self):
        self.assertEqual(self.institution_info.state, "Paraná")
        self.assertEqual(self.institution_info.city, "Curitiba")
        self.assertEqual(self.institution_info.phone, "4199999999")
        self.assertEqual(self.institution_info.cep, "81400000")

