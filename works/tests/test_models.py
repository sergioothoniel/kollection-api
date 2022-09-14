from django.test import TestCase
from works.models import Work
from users.models import User

from model_bakery import baker


class WorkTestModel(TestCase):
    @classmethod
    def setUp(cls):
        cls.work_info = baker.make_recipe("works.work_info_test")
        cls.work = baker.make_recipe("works.work_test", infos_id=cls.work_info.id)

    def test_fields_work(self):
        self.assertIs(self.work.name, "Trabalho Backend")
        self.assertIs(self.work_info_id, self.work_info.id)

    def tests_fields_work_infos(self):
        self.assertEqual(self.institution_info.knowledge_area, "Tecnologia")
        self.assertEqual(self.institution_info.title, "desenvolvendo algo")
        self.assertEqual(self.institution_info.summary, "test")
        self.assertEqual(self.institution_info.link, "htttp://test")
        self.assertEqual(self.institution_info.visibility, "Intern")
        self.assertEqual(self.institution_info.is_reviewed, True)
        self.assertEqual(self.institution_info.is_active, True)
