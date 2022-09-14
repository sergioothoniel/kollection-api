from django.test import TestCase
from model_bakery import baker
from works.models import Work


class WorkTestModel(TestCase):
    @classmethod
    def setUp(cls):
        cls.work = baker.make(Work)

    def test_fields_work_type(self):

        self.assertIs(type(self.work.title), str)
        self.assertIs(type(self.work.knowledge_area), str)

    def test_fields_work_length(self):

        max_length_title = self.work._meta.get_field("title").max_length
        max_length_knowledge_area = self.work._meta.get_field(
            "knowledge_area"
        ).max_length

        self.assertEqual(max_length_title, 50)
        self.assertEqual(max_length_knowledge_area, 50)
